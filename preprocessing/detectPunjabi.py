import re
import fasttext
import pandas as pd

OUTPUT_FILE = "data/punjabi_comments.csv"

GURMUKHI_REGEX = re.compile(r'[\u0A00-\u0A7F]')
ROMAN_PUNJABI_WORDS = {
"banda", "kudi", "munda", "tusi", "asi", "eh", "ohna", "sada", "ohda", "usda", "tuhada",
"gabhru", "mutiyar", "jana", "changa", "kithay", "kithon", "kad", "kinna", "kinne", "kaun",
"hun", "baad", "sarson", "chitta", "yaar", "sikh", "dhanvaad", "gal", "kar", "aa",
"pind", "thalle", "naal", "kol", "nerhe", "jutti", "pag", "chunni", "siir", "naak", "munh",
"huth", "shor", "ghatt", "ik", "do", "tin", "char", "panj", "chhe", "sat", "ath", "nau", "das",
"bhukh", "thakya", "ho",
"puttar", "dhee", "vyaah", "bhul", "soch", "rab", "waheguru", "kismat", "sabra", "shukar",
"rehmat", "le", "de", "ban", "reh", "mil", "chhad", "phad", "maar", "lok", "lokan",
"jhagda", "maada", "sohna", "aukha", "bhola", "chhaan",
"kiven", "kirtan", "shabad", "pangra", "giddha", "boliyan", "tappe", "yaari", "nibh",
"tor", "shaan", "sochni", "vakhra", "sanjha", "judaa", "thokar", "aas", "khadna", "behna",
"faddna", "sutna", "jagna", "tarna", "dubna", "lachak", "narmi", "sat sri akal",
"pichhon", "samne", "pairan", "haathan", "akhiyan", "munde", "kudiyan", "gharwali",
"gharwala", "shehri", "chulha", "behni", "firdi", "phirni", "langar", "sangat", "panth",
"rehat", "maryada", "sehaj", "bhog", "ardaas", "gurudwara",
"appah", "kam", "ae", "ve", "ni", "ji", "haan", "haanji", "nai", "nahi", "kyonki", "bas",
"hi", "vi", "tan", "te", "fer", "phir", "jad", "jado", "thoda", "zyada",
"bahla", "bahli", "bahle", "bahut",
"lagda", "lagdi", "lagde", "laggi", "lagge", "samajh",
"milda", "mildi", "milde", "milla", "mille",
"aaya", "aayi", "aaye",
"jaanda", "jaandi", "jaande",
"karda", "kardi", "karde",
"kitta", "kitti", "kittay",
"rehnda", "rehndi", "rehnde",
"kehnda", "kehndi", "kehnde",
"bolda", "boldi", "bolde",
"puchda", "puchdi", "puchde",
"dekheya", "dekhi", "dekhe",
"suneya", "suni", "sune",
"sachcha", "jhootha", "saf", "ganda", "maja", "mazedaar",
"tedha", "seedha", "ghussa", "pyaar", "nafrat",
"thand", "garmi", "bheed",
"bheja", "akal", "tez", "mandi", "sasti", "mehngi",
"punjab", "punjabi", "sardaar", "sardarni", "singh", "kaur",
"pagg", "khanda", "kes", "keski", "kirpan", "takht",
"amrit", "pyare",
"jat", "jatt", "jatti", "khatri", "ramgarhia",
"malwa", "majha", "doaba",
"wah", "shabaash", "ohho", "uff", "arey", "oye", "haye",
"mazza", "ghaint", "att", "kaint", "bura", "vadiya",
"chardi", "kala",
"ithe", "uthe", "othay", "ethe", "jithe", "kade", "kadi",
"subah", "shaam", "raat", "din",
"maa", "baapu", "bebe", "veer", "bhain", "pra",
"rishta", "saaka", "biradari",
"waheguru ji ka khalsa", "waheguru ji ki fateh",
"akal purakh", "guru granth sahib", "sacha paatshah",
"apna", "apni", "apne", "sadda", "saddi", "sadde",
"tuhanu", "menu", "mainu", "enu", "onu",
"ethevi", "uthevi", "ithonvi",
"kyun", "kyonvi", "jaive", "jiven", "jinna",
"viha", "horvi", "thaan", "thavaan",
"hoya", "hoyi", "hoye",
"baneya", "banayi", "banaye",
"marya", "mari", "mare",
"phaddeya", "phaddi", "phadde",
"chhadeya", "chhadi", "chhade",
"leya", "layi", "laye",
"ditta", "ditti", "ditte",
"peya", "payi", "paye",
"beshak", "laaj", "sharam", "izzat",
"naram", "sakht", "kacha", "pakka",
"chota", "vada", "vadda", "nikka",
"sohnaai", "roop", "rangla",
"fikar", "chinta", "khushi", "dukh", "rona", "hassna",
"kaand", "attwaadi", "bawaal",
"khait", "fasal", "mitti", "paani", "nalka", "toka",
"khetan", "tralli", "charkha", "rassi", "boraan",
"tau", "taayi", "chacha", "chachi",
"maasi", "maasa", "phupha", "phuphi",
"jija", "saali", "devar", "nanad",
"geet", "gaana", "sur", "taal",
"josh", "vair", "daaru","jor",
"balle", "chakde","laa","ke", 
"chak de phatte", "balle balle", "jor laa ke", "att hi att"
}

model = fasttext.load_model("models/lid.176.bin")

def is_gurmukhi(text):
    return bool(GURMUKHI_REGEX.search(text))

def is_roman_punjabi(text, threshold=2):
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    matches = sum(1 for w in words if w in ROMAN_PUNJABI_WORDS)
    return matches >= threshold

def detect_language(text):
    labels, probs = model.predict(text, k=10)
    plang = ["pa", "pan","pnb", "ur", "hi", "hif"]
    for i in range(len(labels)):
        lang = labels[i].replace("__label__", "")
        confidence = probs[i]
        if lang in plang and confidence >= 0.2:
            return True
    return False

def is_punjabi(text):
    if is_gurmukhi(text):
        return True
    if is_roman_punjabi(text):
        return True
    if detect_language(text):
        return True
    return False    
    
df = pd.read_csv("data/clean_comments.csv")
df["clean_text"] = df["clean_text"].fillna("").astype(str)
df["is_punjabi"] = df["clean_text"].apply(is_punjabi)
df = df[["clean_text", "published_at", "is_punjabi"]]

punjabi_df = df[df["is_punjabi"] == True]
punjabi_df = punjabi_df[["clean_text", "published_at"]]
punjabi_df.to_csv(OUTPUT_FILE, index=False)

print(f"Punjabi comments: {(len(punjabi_df) / len(df)):.3f} ({len(punjabi_df)})")
