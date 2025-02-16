from jacodemon.manager import UIState

class AppController:

    def __init__(self):
        self.current_state = UIState.CONFIG

    def set_state(self, new_state):
        if self.current_state.can_transition_to(new_state):
            self.current_state = new_state
            self.ui_manager.set_state(new_state)
        else:
            raise Exception(f"Cannot transition from {self.current_state} to {new_state}")

    def on_dialog_exit(self, ok: bool):

        if self.current_state == UIState.CONFIG:
            if ok:
                self.set_state(UIState.SELECT_MAP)
            else:
                self.set_state(UIState.CONFIG)

        elif self.current_state == UIState.SELECT_MAP:
            if ok:
                self.set_state(UIState.PRE_LAUNCH)
            else:
                self.set_state(UIState.CONFIG)

        elif self.current_state == UIState.PRE_LAUNCH:
            if ok:
                self.set_state(UIState.SUBPROCESS_RUNNING)
            else:
                self.set_state(UIState.SELECT_MAP)

        else:
            raise Exception(f"Unknown state {self.current_state}")
