import json
import sys

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print('nope')
        exit(1)

    # get parameters
    correct_proof_file = sys.argv[1]
    malicious_proof_conf_file = sys.argv[2]
    malicious_proof_output_file = sys.argv[3]

    # read in data
    edited_proof_content = {}
    malicious_proof_content = {}
    with open('./test/test_data/{}'.format(correct_proof_file), 'r') as r_correct_proof_file:
        edited_proof_content = json.loads(r_correct_proof_file.read())
    
    with open('./test/test_data/{}'.format(malicious_proof_conf_file), 'r') as r_malicious_proof_conf_file:
        malicious_proof_content = json.loads(r_malicious_proof_conf_file.read())
    
    # replace correct with malicious data
    for i in range(len(malicious_proof_content['index'])):
        index = malicious_proof_content['index'][i]
        edited_proof_content['inputs'][index] = malicious_proof_content['malformedInput'][i]

    # write to output file
    with open('./test/test_data/{}'.format(malicious_proof_output_file), 'w') as w_malicious_proof_output_file:
        w_malicious_proof_output_file.write(json.dumps(edited_proof_content, sort_keys=True, indent=4))