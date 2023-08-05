#!/usr/bin/python3

import datetime, os, unittest

from slippi import Game, parse
from slippi.metadata import Metadata
from slippi.id import InGameCharacter, CSSCharacter, Stage
from slippi.event import Start, End, Frame, Buttons, Triggers, Position, ParseEvent


BPhys = Buttons.Physical
BLog = Buttons.Logical


def norm(f):
    return 1 if f > 0.01 else -1 if f < -0.01 else 0


def path(name):
    return os.path.join(os.path.dirname(__file__), 'replays', name + '.slp')


class TestGame(unittest.TestCase):
    def _game(self, name):
        return Game(path(name))

    def _stick_seq(self, game):
        pass

    # not used yet because the recorder currently puts bogus values in triggers.physical
    def _trigger_seq(self, game):
        last_triggers = None
        trigger_seq = []
        for frame in game.frames:
            t = frame.ports[0].leader.pre.triggers
            t = Triggers(norm(t.logical), norm(t.physical.l), norm(t.physical.r))
            if (t.logical or t.physical.l or t.physical.r) and t != last_triggers:
                trigger_seq.append(t)
            last_triggers = t
        return trigger_seq

    def _button_seq(self, game):
        last_buttons = None
        button_seq = []
        for frame in game.frames:
            b = frame.ports[0].leader.pre.buttons
            if (b.logical or b.physical) and b != last_buttons:
                button_seq.append(b)
            last_buttons = b
        return button_seq

    def test_slippi_old_version(self):
        game = self._game('v0.1')
        self.assertEqual(game.start.slippi.version, Start.Slippi.Version(0,1,0,0))
        self.assertEqual(game.metadata.duration, None)
        self.assertEqual(game.metadata.players, (None, None, None, None))
        self.assertEqual(game.start.players[0].character, CSSCharacter.FOX)
        self.assertEqual(game.start.players[1].character, CSSCharacter.GANONDORF)

    def test_game(self):
        game = self._game('game')

        self.assertEqual(game.metadata, Metadata._parse({
            'startAt': '2018-06-22T07:52:59Z',
            'lastFrame': 5085,
            'playedOn': 'dolphin',
            'players': {
                '0': {'characters': {InGameCharacter.MARTH: 5209}},
                '1': {'characters': {InGameCharacter.FOX: 5209}}}}))
        self.assertEqual(game.metadata, Metadata(
            date=datetime.datetime(2018, 6, 22, 7, 52, 59, 0, datetime.timezone.utc),
            duration=5209,
            platform=Metadata.Platform.DOLPHIN,
            players=(
                Metadata.Player({InGameCharacter.MARTH: 5209}),
                Metadata.Player({InGameCharacter.FOX: 5209}),
                None, None)))

        self.assertEqual(game.start, Start(
            is_teams=False,
            random_seed=3803194226,
            slippi=Start.Slippi(Start.Slippi.Version(1,0,0,0)),
            stage=Stage.YOSHIS_STORY,
            players=(
                Start.Player(character=CSSCharacter.MARTH, type=Start.Player.Type.HUMAN, stocks=4, costume=3, team=None, ucf=Start.Player.UCF(False, False)),
                Start.Player(character=CSSCharacter.FOX, type=Start.Player.Type.CPU, stocks=4, costume=0, team=None, ucf=Start.Player.UCF(False, False)),
                None, None)))

        self.assertEqual(game.end, End(End.Method.CONCLUSIVE))

        self.assertEqual(game.metadata.duration, len(game.frames))

    def test_ics(self):
        game = self._game('ics')
        self.assertEqual(game.metadata.players[0].characters, {
            InGameCharacter.NANA: 344,
            InGameCharacter.POPO: 344})
        self.assertEqual(game.start.players[0].character, CSSCharacter.ICE_CLIMBERS)
        self.assertIsNotNone(game.frames[0].ports[0].follower)

    def test_ucf(self):
        self.assertEqual(self._game('shield_drop').start.players[0].ucf, Start.Player.UCF(dash_back=False, shield_drop=True))
        self.assertEqual(self._game('dash_back').start.players[0].ucf, Start.Player.UCF(dash_back=True, shield_drop=False))

    def test_buttons_lrzs(self):
        game = self._game('buttons_lrzs')
        self.assertEqual(self._button_seq(game), [
            Buttons(BLog.TRIGGER_ANALOG, BPhys.NONE),
            Buttons(BLog.TRIGGER_ANALOG|BLog.L, BPhys.L),
            Buttons(BLog.TRIGGER_ANALOG, BPhys.NONE),
            Buttons(BLog.TRIGGER_ANALOG|BLog.R, BPhys.R),
            Buttons(BLog.TRIGGER_ANALOG|BLog.A|BLog.Z, BPhys.Z),
            Buttons(BLog.START, BPhys.START)])

    def test_buttons_abxy(self):
        game = self._game('buttons_abxy')
        self.assertEqual(self._button_seq(game), [
            Buttons(BLog.A, BPhys.A),
            Buttons(BLog.B, BPhys.B),
            Buttons(BLog.X, BPhys.X),
            Buttons(BLog.Y, BPhys.Y)])

    def test_dpad_udlr(self):
        game = self._game('dpad_udlr')
        self.assertEqual(self._button_seq(game), [
            Buttons(BLog.DPAD_UP, BPhys.DPAD_UP),
            Buttons(BLog.DPAD_DOWN, BPhys.DPAD_DOWN),
            Buttons(BLog.DPAD_LEFT, BPhys.DPAD_LEFT),
            Buttons(BLog.DPAD_RIGHT, BPhys.DPAD_RIGHT)])

    def test_cstick_udlr(self):
        game = self._game('cstick_udlr')
        self.assertEqual(self._button_seq(game), [
            Buttons(BLog.CSTICK_UP, BPhys.NONE),
            Buttons(BLog.CSTICK_DOWN, BPhys.NONE),
            Buttons(BLog.CSTICK_LEFT, BPhys.NONE),
            Buttons(BLog.CSTICK_RIGHT, BPhys.NONE)])

    def test_joystick_udlr(self):
        game = self._game('joystick_udlr')
        self.assertEqual(self._button_seq(game), [
            Buttons(BLog.JOYSTICK_UP, BPhys.NONE),
            Buttons(BLog.JOYSTICK_DOWN, BPhys.NONE),
            Buttons(BLog.JOYSTICK_LEFT, BPhys.NONE),
            Buttons(BLog.JOYSTICK_RIGHT, BPhys.NONE)])

    def test_nintendont(self):
        game = self._game('nintendont')
        self.assertEqual(game.metadata.platform, Metadata.Platform.NINTENDONT)

    def test_netplay_name(self):
        game = self._game('netplay_name')
        players = game.metadata.players
        self.assertEqual(players[0].netplay_name, 'Player1')
        self.assertEqual(players[1].netplay_name, 'metonym')

    def test_console_name(self):
        game = self._game('console_name')
        self.assertEqual(game.metadata.console_name, 'Station 1')

    def test_metadata_json(self):
        game = self._game('game')
        self.assertEqual(game.metadata_raw, {
            'lastFrame': 5085,
            'playedOn': 'dolphin',
            'players': {
                '0': {'characters': {'18': 5209}},
                '1': {'characters': {'1': 5209}}},
            'startAt': '2018-06-22T07:52:59Z'})

    def test_v2(self):
        game = self._game('v2.0')
        self.assertEqual(game.start.slippi.version, Start.Slippi.Version(2,0,1))

    def test_unknown_event(self):
        with self.assertWarns(Warning):
            game = self._game('unknown_event')


class TestParse(unittest.TestCase):
    def test_parse(self):
        metadata = None
        def set_metadata(x):
            nonlocal metadata
            metadata = x
        parse(path('game'), {ParseEvent.METADATA: set_metadata})
        self.assertEqual(metadata.duration, 5209)


if __name__ == '__main__':
    unittest.main()
