import os
import json
import sys

def main():
    labels_to_apply = {
        "Q01": {
            "DOC_134": 0, "DOC_110": 0, "DOC_091": 0, "DOC_061": 0,
            "DOC_136": 0, "DOC_112": 0, "DOC_045": 0, "DOC_147": 0, "DOC_123": 0
        },
        "Q02": {
            "DOC_117": 0, "DOC_159": 0, "DOC_130": 0, "DOC_106": 0,
            "DOC_006": 1, "DOC_110": 0, "DOC_134": 0, "DOC_193": 0
        },
        "Q03": {
            "DOC_159": 0, "DOC_188": 0, "DOC_040": 0, "DOC_160": 0
        },
        "Q04": {
            "DOC_035": 1, "DOC_054": 0, "DOC_036": 0
        },
        "Q05": {
            "DOC_164": 0, "DOC_008": 0, "DOC_167": 0, "DOC_002": 0
        },
        "Q06": {
            "DOC_095": 0, "DOC_147": 0, "DOC_123": 0, "DOC_114": 0, "DOC_138": 0
        },
        "Q07": {
            "DOC_061": 0, "DOC_091": 0, "DOC_141": 0, "DOC_117": 0, "DOC_169": 0
        },
        "Q08": {
            "DOC_081": 0, "DOC_035": 1, "DOC_038": 0, "DOC_135": 0, "DOC_111": 0
        },
        "Q09": {
            "DOC_133": 0, "DOC_109": 0, "DOC_125": 0, "DOC_101": 0
        },
        "Q10": {
            "DOC_008": 0, "DOC_144": 0, "DOC_120": 0, "DOC_167": 0, "DOC_055": 1
        },
        "Q11": {
            "DOC_142": 0, "DOC_118": 0, "DOC_072": 0, "DOC_038": 0
        },
        "Q12": {
            "DOC_008": 0, "DOC_002": 0, "DOC_198": 0, "DOC_200": 0, "DOC_193": 0, "DOC_192": 0
        },
        "Q13": {
            "DOC_008": 0, "DOC_170": 0, "DOC_047": 0, "DOC_151": 0
        },
        "Q14": {
            "DOC_029": 0, "DOC_197": 0, "DOC_170": 0
        },
        "Q15": {
            "DOC_090": 0, "DOC_082": 0, "DOC_200": 0, "DOC_198": 0, "DOC_199": 0, "DOC_192": 0, "DOC_191": 0
        }
    }

    file_path = os.path.join(os.path.dirname(__file__), 'results/pooled_evaluation_v4.json')
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    total_candidates = 0
    newly_labeled = 0
    previously_labeled = 0
    remaining_nulls = 0
    modified_existing = 0

    for q in data:
        q_id = q['query_id']
        for cand in q['pooled_candidates']:
            doc_id = cand['doc_id']
            current_rel = cand['relevance']
            total_candidates += 1
            
            if current_rel is None:
                if q_id in labels_to_apply and doc_id in labels_to_apply[q_id]:
                    cand['relevance'] = labels_to_apply[q_id][doc_id]
                    newly_labeled += 1
                else:
                    remaining_nulls += 1
                    print(f"ERROR: Missing label for {q_id} {doc_id}")
            else:
                previously_labeled += 1
                # Check if we accidentally try to modify an existing one
                if q_id in labels_to_apply and doc_id in labels_to_apply[q_id]:
                    modified_existing += 1

    print("VALIDATION REPORT")
    print(f"- {total_candidates} total candidates")
    print(f"- {newly_labeled} newly labeled")
    print(f"- {previously_labeled} previously labeled")
    print(f"- {remaining_nulls} remaining nulls")
    print(f"- {modified_existing} modified existing labels")

    if remaining_nulls == 0 and modified_existing == 0 and newly_labeled == 76 and previously_labeled == 149 and total_candidates == 225:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print("\nValidation passed. File successfully updated.")
    else:
        print("\nValidation failed. File not updated.")
        sys.exit(1)

if __name__ == "__main__":
    main()
