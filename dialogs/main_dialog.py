## This Bot is based on the examples provided by the Microsoft Azure team.
## A version of the original code examples can be found on the Microsoft Github-repo here: https://github.com/microsoft/BotBuilder-Samples
## Licensed under the MIT License.

## - Project Info -
# Github-repo: https://github.com/codingPotato69/CSC408-ASSI1
# Contributors: 
#       1- Adnan Youssef
#       2- Naji Mohammed
#       3- Omar Ahmed
## Licensed under the MIT License.

from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.core import MessageFactory, UserState

from data_models import UserProfile
from dialogs.top_level_dialog import TopLevelDialog


class MainDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(MainDialog, self).__init__(MainDialog.__name__)

        self.user_state = user_state

        self.add_dialog(TopLevelDialog(TopLevelDialog.__name__))
        self.add_dialog(
            WaterfallDialog("WFDialog", [self.initial_step, self.final_step])
        )

        self.initial_dialog_id = "WFDialog"

    async def initial_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        return await step_context.begin_dialog(TopLevelDialog.__name__)

    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        user_info: UserProfile = step_context.result

        status = f"Thank you for using the AD-Police guide Bot."

        await step_context.context.send_activity(MessageFactory.text(status))

        # store the UserProfile
        accessor = self.user_state.create_property("UserProfile")
        await accessor.set(step_context.context, user_info)

        # Start a new service dialog
        return await step_context.replace_dialog(MainDialog.__name__, step_context.result)