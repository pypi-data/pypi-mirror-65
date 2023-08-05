import typing as T
from copy import deepcopy

from .wurf import welcher_wurf, Wurf, prioritaet, Schock
from .spieler import Spieler
from .exceptions import (
    ZuWenigSpieler,
    NochNichtGeworfen,
    ZuOftGeworfen,
    FalscherSpieler,
    KeineWuerfeVorhanden,
    UnbekannterSpieler,
    RundeVorbei,
)

NUM_MAX_DECKEL = 15


class WurfEvaluierung(T.NamedTuple):
    prioritaet: float
    wurf_anzahl: int
    reihenfolge: int
    spieler: Spieler
    wurf: Wurf


class SpielzeitStatus(T.NamedTuple):
    deckel_in_topf: int
    spieler: T.List[Spieler]


class RundenDeckelManagement:
    def __init__(self, runden_status: SpielzeitStatus):
        if len(runden_status.spieler) < 2:
            raise ZuWenigSpieler

        self._waren_anfangs_deckel_im_topf = runden_status.deckel_in_topf > 0
        self._zahl_deckel_im_topf = runden_status.deckel_in_topf
        self._spieler = runden_status.spieler
        self._spieler_namen = [S.name for S in self._spieler]
        self._aktueller_spieler_idx = 0
        self._wuerfe = {S.name: [] for S in self._spieler}

    def weiter(self) -> int:
        aktueller_spieler = self._spieler_namen[self._aktueller_spieler_idx]
        if not self._wuerfe[aktueller_spieler]:
            raise NochNichtGeworfen
        if self._aktueller_spieler_idx + 1 >= len(self._spieler):
            raise RundeVorbei("Runde ist bereits vorbei!")
        self._aktueller_spieler_idx += 1
        return self._aktueller_spieler_idx

    def deckel_verteilen_restliche_spieler(self) -> SpielzeitStatus:
        hoch, tief = self.hoch_und_tief()
        self._deckel_verteilen(hoch, tief)
        restliche_spieler = self._restliche_spielerinnen_bestimmen(tief.spieler)
        return SpielzeitStatus(self._zahl_deckel_im_topf, restliche_spieler)

    def _deckel_verteilen(self, hoch: WurfEvaluierung, tief: WurfEvaluierung):
        if hoch.wurf is Schock.out:
            self._schockout_verteilen(tief)
        elif self._waren_anfangs_deckel_im_topf:
            self._deckel_im_topf_verteilen_hoch_tief(hoch, tief)
        else:
            self._deckel_von_hoch_an_tief_verteilen(hoch, tief)

    def _deckel_im_topf_verteilen_hoch_tief(
        self, hoch: WurfEvaluierung, tief: WurfEvaluierung
    ):
        anzahl_deckel = hoch.wurf.deckel_wert
        self._deckel_im_topf_verteilen(tief.spieler, anzahl_deckel)

    def _deckel_im_topf_verteilen(self, spieler: Spieler, anzahl_deckel: int):
        anzahl_deckel = min(self._zahl_deckel_im_topf, anzahl_deckel)
        self._zahl_deckel_im_topf -= anzahl_deckel
        spieler.deckel += anzahl_deckel

    def _deckel_von_hoch_an_tief_verteilen(
        self, hoch: WurfEvaluierung, tief: WurfEvaluierung
    ):
        self._deckel_von_spieler_an_spieler(
            geber=hoch.spieler,
            empfaenger=tief.spieler,
            anzahl_deckel=hoch.wurf.deckel_wert,
        )

    def _deckel_von_spieler_an_spieler(
        self, geber: Spieler, empfaenger: Spieler, anzahl_deckel: int
    ):
        anzahl_deckel = min(geber.deckel, anzahl_deckel)
        geber.deckel -= anzahl_deckel
        empfaenger.deckel += anzahl_deckel

    def _schockout_verteilen(self, tief: WurfEvaluierung):
        zahl_verteile_deckel = sum(s.deckel for s in self._spieler)
        zahl_alle_deckel = self._zahl_deckel_im_topf + zahl_verteile_deckel
        self._zahl_deckel_im_topf = 0
        for s in self._spieler:
            s.deckel = 0
        tief.spieler.deckel = zahl_alle_deckel

    def _restliche_spielerinnen_bestimmen(self, verlierer: Spieler) -> T.List[Spieler]:
        spielerinnen = [s for s in self._spieler if self._noch_im_spiel(s)]
        start_idx = spielerinnen.index(verlierer)
        spielerinnen = spielerinnen[start_idx:] + spielerinnen[:start_idx]
        return spielerinnen

    def _noch_im_spiel(self, spielerin):
        return self._zahl_deckel_im_topf or spielerin.deckel

    def wurf(
        self,
        spieler_name: str,
        augen: T.Tuple[int, int, int],
        aus_der_hand: bool = True,
    ) -> WurfEvaluierung:
        try:
            spieler_idx = self._spieler_namen.index(spieler_name)
        except ValueError as err:
            raise UnbekannterSpieler(spieler_name) from err

        if spieler_idx != self._aktueller_spieler_idx:
            aktueller_spieler = self._spieler_namen[self._aktueller_spieler_idx]
            raise FalscherSpieler(
                f"{spieler_name} hat geworfen, {aktueller_spieler} war aber dran!"
            )

        bestehende_wuerfe = self._wuerfe[spieler_name]
        if len(bestehende_wuerfe) >= self.num_maximale_wuerfe:
            raise ZuOftGeworfen()

        wurf = welcher_wurf(augen, aus_der_hand)
        bestehende_wuerfe.append(wurf)

        return WurfEvaluierung(
            prioritaet(wurf),
            wurf_anzahl=len(bestehende_wuerfe),
            reihenfolge=spieler_idx,
            spieler=self._spieler[spieler_idx],
            wurf=wurf,
        )

    def ist_lust_wurf(self, wurf: WurfEvaluierung):
        if wurf.wurf_anzahl <= 1 or wurf.reihenfolge == 0:
            return False
        simulation = deepcopy(self)
        verteilung = simulation.deckel_verteilen_restliche_spieler()
        waere_raus = wurf.spieler not in verteilung.spieler
        return waere_raus

    def strafdeckel_verteilen(self, bestrafte: Spieler):
        if self._waren_anfangs_deckel_im_topf:
            self._deckel_im_topf_verteilen(bestrafte, 1)
        else:  # spieler mit den meisten Deckeln gibt ab
            deckel = [s.deckel for s in self._spieler]
            meiste_deckel_index = deckel.index(max(deckel))
            geber = self._spieler[meiste_deckel_index]
            self._deckel_von_spieler_an_spieler(geber, bestrafte, 1)
        # NOTE: Auslegungssache. Falls der bestrafte keinen Deckel bekommen hat, zb wenn
        # es keinen Deckel mehr im Topf gab, und nächste Runde trotzdem spielen müsste,
        # dann muss hier entsprechendes `spieler.bestraft` flag gesetzt werden, dass
        # dann in `_restliche_spielerinnen_bestimmen()` abgefragt werden muss.

    def hoch_und_tief(self) -> T.Tuple[WurfEvaluierung, WurfEvaluierung]:
        erster_spieler = self._spieler_namen[0]
        if not self._wuerfe[erster_spieler]:
            raise KeineWuerfeVorhanden()

        evaluierungen = []
        for idx, spieler in enumerate(self._spieler):
            bestehende_wuerfe = self._wuerfe[spieler.name]
            if not bestehende_wuerfe:
                break
            letzter_wurf = bestehende_wuerfe[-1]
            evaluierung = WurfEvaluierung(
                prioritaet=prioritaet(letzter_wurf),
                wurf_anzahl=len(bestehende_wuerfe),
                reihenfolge=idx,
                spieler=spieler,
                wurf=letzter_wurf,
            )
            evaluierungen.append(evaluierung)
        # hoch: index 0, tief: index -1
        evaluierungen.sort(key=self._schockout_reihenfolge_fix)
        return evaluierungen[0], evaluierungen[-1]

    @staticmethod
    def _schockout_reihenfolge_fix(evaluierung: WurfEvaluierung):
        """Schocks werden in umgekehrter Reihenfolge gewertet"""
        if evaluierung.wurf is Schock.out:
            evaluierung = WurfEvaluierung(
                prioritaet=evaluierung.prioritaet,
                wurf_anzahl=evaluierung.wurf_anzahl,
                reihenfolge=-evaluierung.reihenfolge,  # NOTE: Reihenfolge umgekehrt
                spieler=evaluierung.spieler,
                wurf=evaluierung.wurf,
            )
        return evaluierung

    @property
    def num_maximale_wuerfe(self):
        if self._aktueller_spieler_idx == 0:
            return 3
        else:
            start_spieler_name = self._spieler_namen[0]
            wuerfe_start_spieler = self._wuerfe[start_spieler_name]
            num_wuerfe_start_spieler = len(wuerfe_start_spieler)
            return num_wuerfe_start_spieler

    @property
    def aktiver_spieler(self):
        return self._spieler[self._aktueller_spieler_idx]
