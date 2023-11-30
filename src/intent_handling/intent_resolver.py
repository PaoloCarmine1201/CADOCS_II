from src.intent_handling.cadocs_intent import CadocsIntents
from src.intent_handling.tool_selector import ToolSelector
from src.intent_handling.tools import CsDetectorTool

# the Intent Resolver is used to handle the execution given a predicted intent
class IntentResolver:
    def resolve_intent(self, intent, entities):
        # check if the intent is a Cadocs intent (looking forward to have multiple tools)
        if intent in CadocsIntents:
            # execute csdetector and build smell detection message
            if intent == CadocsIntents.GetSmells or intent == CadocsIntents.GetSmellsDate:
                # we instantiate our strategy context
                tool = ToolSelector(CsDetectorTool())
                # then we execute the selected tool with given entities
                # here the date (if present) is set to the format requested by csDetector
                if len(entities) > 2:
                    split_date = entities[1].split("/")
                    entities[1] = ""+split_date[1]+"/"+split_date[0]+"/"+split_date[2]
                
                results = tool.run(entities)
                print("\n\n\nRESULT IN INTENT RESOLVER", results)
                print("\n\n\n")
                return results
            # build info message
            elif intent == CadocsIntents.Info:
                return []
            # build report message
            elif intent == CadocsIntents.Report:
                return []

        # else if intent in OtherToolIntent