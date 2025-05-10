import json
import os
import time
import re
import numpy

PATH_GAMELOGS = 'logs/'

def get_unwanted_logs_list (path_to_file: str):
    unwanted_logs_list = []
    with open(path_to_file, 'r') as f:
        for line in f:
            unwanted_logs_list += [line.replace('\n','')]
    return unwanted_logs_list

def get_elapsed_time(starting_turn: str, ending_turn: str, gamelog: dict) -> time.localtime:
    starting_time = time.mktime(time.strptime((gamelog[starting_turn]["date"])))
    ending_time = time.mktime(time.strptime((gamelog[ending_turn]["date"])))

    return ending_time-starting_time

def get_turns_to_complete_objective(gamelog: dict) -> int:
    max_turns = int(list(gamelog.keys())[-1])
    index = 1
    found = False

    while not found and index < max_turns:
        if  "🎯" in gamelog[str(index)]["narration"]:
            found = True
        else:
            index += 1
    
    return index
        

def get_times_between_turns(gamelog: dict):
    turns = get_turns_to_complete_objective (gamelog)

    deltas = []
    for i in range(0,turns):
        deltas += [time.mktime(time.strptime((gamelog[str(i+1)]["date"]))) - time.mktime(time.strptime((gamelog[str(i)]["date"])))]

    return deltas 

def statistic_summary (values: list):
    summary = {
        "min": numpy.min(values),
        "max": numpy.max(values),
        "mean": numpy.mean(values)
    }
    
    return summary


def get_narrations_length(gamelog: dict, include_starting_narration: bool = True):
    turns = get_turns_to_complete_objective(gamelog)
    narrations_length = []

    if include_starting_narration:
        narrations_length = [len(gamelog["0"]["starting_narration"])]

    for i in range(1,turns+1):
        narrations_length += [len(gamelog[str(i)]["narration"])]

    return narrations_length

def generate_txt_from_gamelog(gamelog):
    number_of_turns = get_turns_to_complete_objective(gamelog)
    print(gamelog["0"]["date"])

    turns_text = ""
    for turn in range(1,number_of_turns+1):
        turns_text+= f'\n======= TURN {str(turn)} ======='
        turns_text+= f'\n\n🔙 Previous world state:\n{gamelog[str(turn)]["previous_rendered_world_state"]}'
        turns_text+= f'\n👉 Input: "{gamelog[str(turn)]["user_input"]}"'
        turns_text+= f'\n\n⚙️ Predicted outcomes:\n{gamelog[str(turn)]["predicted_outcomes"]}'
        turns_text+= f'\n📖 Narration:\n"{gamelog[str(turn)]["narration"].replace("\n","")}"'
        turns_text+= f'\n\n🌐 Updated world state:\n{gamelog[str(turn)]["updated_rendered_world_state"]}'

    text = f"Traza original: {log_filename}\n\n"
    text += f"Jugador: {gamelog["nickname"]}\n"
    text += f"Escenario: {gamelog["world_id"]}\n"
    text += f"Turnos: {str(number_of_turns)}\n"
    text += f"¿Terminado?: {"✅" if "🎯" in gamelog[str(number_of_turns)]["narration"] else "❌"}\n\n"
    text += f"Tiempo desde el inicio del sistema: {time.localtime(get_elapsed_time("0",str(number_of_turns), gamelog)).tm_min} minutos y {time.localtime(get_elapsed_time("0",str(number_of_turns), gamelog)).tm_sec} segundos\n"
    text += f"Tiempo desde el primer mensaje: {time.localtime(get_elapsed_time("1",str(number_of_turns), gamelog)).tm_min} minutos y {time.localtime(get_elapsed_time("0",str(number_of_turns), gamelog)).tm_sec} segundos\n"
    text += f"Tiempo del turno más corto: {"{:.2f}".format(statistic_summary(get_times_between_turns(gamelog))["min"])} segundos\n"
    text += f"Tiempo promedio entre turnos: {"{:.2f}".format(statistic_summary(get_times_between_turns(gamelog))["mean"])} segundos\n"
    text += f"Tiempo del turno más largo: {"{:.2f}".format(statistic_summary(get_times_between_turns(gamelog))["max"])} segundos\n"
    text += turns_text
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text



if __name__ == "__main__":

    unwanted_logs = get_unwanted_logs_list(os.path.join(PATH_GAMELOGS,'do_not_process_these_logs.txt'))

    for log_filename in os.listdir(PATH_GAMELOGS):
        if log_filename.endswith(".json") and log_filename not in unwanted_logs:
            with open(os.path.join(PATH_GAMELOGS,log_filename), 'r', encoding='utf-8') as f:
                gamelog = json.load(f)

            gamelog_as_text = generate_txt_from_gamelog(gamelog)

            with open (os.path.join(PATH_GAMELOGS, log_filename[:-5] + '.txt'), 'w', encoding='utf-8') as f:
                f.write(gamelog_as_text)
                print(f"{log_filename} ({gamelog["nickname"]}) ...done")