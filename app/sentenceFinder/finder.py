import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="tatoeba",
    user="postgres",
    password="postgres")

preparation_query = """
	prepare find(text, text) as
	select s."text" 
	from sentences s
	where s."text" ilike concat('%',$1,'%', $2, '%')
	or s."text" ilike concat('%',$1,'%', $2, '%')
"""

cursor = conn.cursor()
cursor.execute(preparation_query)

base_query = "execute find(%s, %s)"

def find_sentences(h, t):
	cursor.execute(base_query, (h, t))
	return [response[0] for response in cursor.fetchall()]

def prepare_sentences(h,t):
	sentences = find_sentences(h,t)
	marker = sentence_marker(h,t)
	return [marker(sentence) for sentence in sentences]



def sentence_marker(word1, word2):
	def mark_sentence(sentence):
		marked = {'text': sentence}
		pos_h = sentence.lower().find(word1.lower())
		marked['h'] = {'pos': (pos_h, pos_h + len(word1))}
		pos_t = sentence.lower().find(word2.lower())
		marked['t'] = {'pos': (pos_t, pos_t + len(word2))}
		return marked
	return mark_sentence