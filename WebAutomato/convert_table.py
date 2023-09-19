import openai
import pandas as pd


# присваивает колонкам с датой тип datatime
def set_datetime_type(df, format='%d-%m-%Y'):
  for col in df.select_dtypes(object).columns:
    try: 
      df[col] = pd.to_datetime(df[col]).dt.strftime(format)
    except:
      pass
  return df

# формирует запрос к чат гпт
def get_response(content, promt=None, max_tokens=512):
  messages = [{"role": "system", "content": promt}, {"role": "user",  "content": content}] if promt else [{"role": "user",  "content": content}]
  response = openai.ChatCompletion.create(model="gpt-3.5-turbo", 
                                          messages=messages, 
                                          temperature=1,
                                          max_tokens=max_tokens,
                                          top_p=1,
                                          frequency_penalty=0,
                                          presence_penalty=0)
  message = response["choices"][-1]["message"]["content"]
  return message

# преобразует первые 3 строки пандас таблиы в тестовое представление для загрузки в чат гпт
def make_text_tab(df): 
 return f'Headers: {df.columns.tolist()}\nValues:\n{df.head(3).values.tolist()}'

# при помощи чат гпт устанавливает соответствие между колонками изходной таблицы и шаблона. возвращает словарь.
def make_parse_dict(template_df, source_df):
  parse_dict = {}

  source_txt = make_text_tab(source_df) 
  for col in template_df.columns:
    col_txt = f'Header: {col}\nValues:\n{template_df.head(3)[col].to_list()}'
    content = f'there is a table in front of you: {source_txt} tell me the name of the column that contains data most similar to this: {col_txt}'
    
    message = get_response(content)
    
    # ищем название столбца в ответе  
    for parse_col in source_df.columns:
      if message.find(parse_col) != -1:
        parse_dict[parse_col] = col
  return parse_dict




def convert_table(source_path, template_path, target_path, organization, api_key)
  
  openai.organization = organization
  openai.api_key = api_key

  source_df = pd.read_csv(source_path)
  template_df = pd.read_csv(template_path)

  # устанавливаем соответствие между колнками таблицы и шаблона
  parse_dict = make_parse_dict(source_df, template_df)

  # создаём таблицу в соответствии с шаблоном
  target_df = source_df[parse_dict.keys()].rename(columns=parse_dict)

  # Приводим столбцы с датой в соответствие с шаблоном
  target_df = set_datetime_type(target_df)

  # сохраняем результат
  target_df.to_csv(target_path, index=False)
  print(f'Создан фаил: {target_path} \nБыли использованы следующие столбцы: \n{parse_dict}')
