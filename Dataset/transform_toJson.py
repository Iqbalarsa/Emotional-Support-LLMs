import pandas as pd
import json

# Load the data
df_data = pd.read_csv('Dataset/spanish_data.csv') 
df_demo = pd.read_csv('Dataset/spanish_demog.csv')

df_data['post_id'] = df_data['post_id'].astype(str).str.strip()
df_demo['post_id'] = df_demo['post_id'].astype(str).str.strip()


def transform_to_json(df_data, df_demo):
    json_output = []
    unique_posts = df_data['post_id'].unique()
    
    for post_id in unique_posts:
        # Take demographic info
        demo = df_demo[df_demo['post_id'] == post_id]
        
        # Helper function
        def get_val(df, col):
            return df[col].iloc[0] if not df.empty and pd.notna(df[col].iloc[0]) else "unknown"
            
        demo_dict = {
            "settlement": get_val(demo, "settlement"),
            "gender": get_val(demo, "gender"),
            "age": get_val(demo, "age"),
            "born_in": get_val(demo, "born_in"),
            "marital_status": get_val(demo, "marital_status"),
            "number_of_people_in_household": get_val(demo, "number_of_people_in_household"),
            "education": get_val(demo, "education"),
            "profession": get_val(demo, "profession"),
            "employment": get_val(demo, "employement"),
            "social_class": get_val(demo, "social_class"),
            "religion": get_val(demo, "religion")
        }
        
        # Basic structure of data
        post_data = df_data[df_data['post_id'] == post_id]
        post_entry = {
            "culture": post_data['culture'].iloc[0],
            "post_id": post_id,
            "post": {
                "text": post_data['text'].iloc[0],
                "emotional_distress": [],
                "cultural_signals": [],
                "demographic_info": demo_dict
            },
            "response": {
                "emotional_support": [],
                "cultural_signals": [], 
                "empathy_score": "unknown"
            }
        }
        
        for _, row in post_data.iterrows():
            if row['level'] == 'post':
                if row['category'] == 'emotional_distress':
                    post_entry['post']['emotional_distress'].append({"phrase": row['phrase'], "intensity": row['intensity'] if pd.notna(row['intensity']) else "unknown"})
                elif row['category'] == 'cultural_signals':
                    post_entry['post']['cultural_signals'].append({"phrase": row['phrase'], "type": row['type'] if pd.notna(row['type']) else "unknown"})
            
            elif row['level'] == 'response':
                if row['category'] == 'emotional_support':
                    post_entry['response']['emotional_support'].append({"phrase": row['phrase'], "strategy": row['strategy'] if pd.notna(row['strategy']) else "unknown"})
                
                elif row['category'] == 'cultural_signals':
                    post_entry['response']['cultural_signals'].append({"phrase": row['phrase'], "type": row['type'] if pd.notna(row['type']) else "unknown"})
                
                elif row['category'] == 'emphaty_score':
                    post_entry['response']['empathy_score'] = str(row['emphaty_score'])
                    
        json_output.append(post_entry)
    return json_output

result = transform_to_json(df_data, df_demo)

with open('dataset_spanish.jsonl', 'w', encoding='utf-8') as f:
    for entry in result:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')
