from class_node import Node
from random import randint


def generate_nodes():
    list_of_nodes = []
    global value
    value = generate_random_array(number_of_nodes, zero_decision_ratio)
    for node_id in range(number_of_nodes):
        list_of_nodes.append(Node(node_id=node_id, initial_value=value[node_id], number_of_nodes=number_of_nodes, r=r))
    return list_of_nodes

def generate_messages_list(): # all nodes generate the message
    messages = []
    for node_id in range(len(nodes)):
        messages.append(nodes[node_id].generate_message())
    return messages

def generate_random_array(length, zero_ratio):
    random_array = []
    for index in range(length):
        random_variable = randint(0, 100)
        random_array.append(0) if random_variable > zero_ratio else random_array.append(1)
    return random_array

def deliver_messages(messages):
    for receiver_node_id in range(number_of_nodes):
        delivery_list = generate_random_array(number_of_nodes, drop_messages_ratio)
        print(delivery_list)
        global drop_message_flag
        for message_index in range(len(messages)):
            for delivery_list_index in range(len(delivery_list)):
                if message_index != delivery_list_index and delivery_list[delivery_list_index] == 1:
                    nodes[receiver_node_id].receive_message(messages[message_index])
                elif delivery_list[delivery_list_index] == 0:
                    drop_message_flag = True

def message_passing_simulation(): # simulate round by round of one simulation
   for any_round in range(r):
       messages = generate_messages_list() # generate the list of all messages that nodes should send in that round
       deliver_messages(messages)

def decision_making():
    for node_index in range(number_of_nodes):
        decisions.append(nodes[node_index].decision_making(r))

def check_validity():
    global false_validity_counter
    if (all(not v for v in value) and all(not d for d in decisions) or
        (not (all(value) and not drop_message_flag)) or
            (any(value) and not all(value))):
        return True
    else:
        false_validity_counter += 1
        return False

def check_agreement():
    global false_agreement_counter
    if all(not decision for decision in decisions) or all(decisions):
        return True
    else:
        false_agreement_counter += 1
        return False

def calculate_validity_agreement_false_ratio():
    v_percentage = false_validity_counter * 1.0 / number_of_simulations
    a_percentage = false_agreement_counter * 1.0/ number_of_simulations
    return a_percentage, v_percentage

def create_table():
    # Print the table with formatting
    print("┌───────┬──────────────────────┬──────────────────────┬────────────┬──────────┐")
    print("│ index │       value          │      decision        │ agreement  │ validity │")
    print("├───────┼──────────────────────┼──────────────────────┼────────────┼──────────┤")

    # Print each row in the table
    for index, row in enumerate(output_data):
        tindex, tvalue, tdecisions, tagreement, tvalidity = row


        if index != len(output_data) - 1:
            # Print the row with formatted and centered data
            print(f"│ {tindex+1:^5} │ {str(tvalue):^20} │ {str(tdecisions):^20} │ {"True" if tagreement == 1 else "False":^10} │ {"True" if tvalidity == 1 else "False":^8} │")
        else:
            tvalidity = f"{tvalidity:.5f}"
            tagreement = f"{tagreement:.5f}"
            print(f"│ {"-":^5} │ {"-":^20} │ {"-":^20} │ {tagreement:^10} │ {tvalidity:^8} │")
    print("└───────┴──────────────────────┴──────────────────────┴────────────┴──────────┘")



if __name__ == "__main__":
    r = int(input("Enter number of rounds : "))
    number_of_nodes = int(input("Enter number of nodes : "))
    number_of_simulations = int(input("Enter number of simulations : "))
    drop_messages_ratio = int(input("Enter success messages ratio (your number / 100) : "))
    zero_decision_ratio = int(input("Enter the ratio of initial 1 decisions (your number / 100) : "))
    output_data = []
    false_validity_counter = 0
    false_agreement_counter = 0
    for i in range(number_of_simulations):
        value = [] # value of all nodes
        nodes = generate_nodes() # generate all nodes and append all nodes initial value into the value[]
        drop_message_flag = False # flag to figure out is any message dropped or not ( uses in validity )
        message_passing_simulation() # simulate massages pass through nodes
        decisions = [] # decisions made by nodes after massages passed
        decision_making() # append all nodes decisions into decisions[]
        validity = check_validity() # validity checker
        agreement = check_agreement() # agreement checker

        # create sample output and add this loop of simulation at the end of simulation's datas
        sample_output = (i, value, decisions, agreement, validity)
        output_data.append(sample_output)
        print(drop_message_flag, )
    agreement_percentage, validity_percentage = calculate_validity_agreement_false_ratio()  # calculate validity and agreement
    # the last line of data should be percentages
    last_line_sample = ("-", "-", "-", agreement_percentage, validity_percentage)
    output_data.append(last_line_sample)
    create_table()