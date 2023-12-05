import torch
from transformers import AutoModelForCausalLM
from transformers import AutoTokenizer
from model_wrapper.gpt2_wrapper import GPT2Wrapper
from llm_automaton.llm_automaton_builder import LLMAutomatonBuilder
from pythautomata.automata_definitions.tomitas_grammars import TomitasGrammars
from automata_examples.man_woman_dfa import get_man_woman_automaton
from pythautomata.model_exporters.dot_exporters.wfa_dot_exporting_strategy import WFADotExportingStrategy

def main():
    torch.manual_seed(42)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model_id = "gpt2"  # Change this to "gpt2" if you get memory issues

    tokenizer = AutoTokenizer.from_pretrained(model_id, use_fast=True)
    model = AutoModelForCausalLM.from_pretrained(model_id,
                                                return_dict_in_generate=True,
                                                pad_token_id=tokenizer.eos_token_id).to(device)

    wrapper = GPT2Wrapper(model, tokenizer, device)
    builder = LLMAutomatonBuilder()
    automaton = builder.construct_llm_automaton(get_man_woman_automaton(), wrapper)

    exporter = WFADotExportingStrategy()
    exporter.export(automaton)
    # automaton.export()


if __name__ == "__main__":
    main()