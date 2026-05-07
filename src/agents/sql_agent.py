"""
SQL Agent - Dogal dil ile veritabani sorgulama.
"""

import sys
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_ollama import ChatOllama

from src.db.database import DATABASE_URL


SISTEM_PROMPT = """You are YapayMusavir, a Turkish tax data assistant.

Your job: Query the SQLite database to answer financial questions in Turkish.

WORKFLOW:
1. Use sql_db_list_tables to see tables
2. Use sql_db_schema to understand columns
3. Use sql_db_query to RUN your SELECT query
4. Read the actual results
5. Write a Turkish answer with the actual numbers

RULES:
- ONLY use SELECT queries
- ALWAYS execute SQL with sql_db_query before answering
- Answer in Turkish, format numbers as "X,XXX.XX TL"
- Be concise

DATABASE:
- giderler: tarih, satici, tutar, kdv_tutari, toplam_tutar, kategori_id, aciklama, odeme_yontemi
- gelirler: tarih, musteri_id, tutar, kdv_tutari, stopaj_tutari, net_tahsilat, kategori_id, odendi
- kategoriler: id, ad, tip ('gider' or 'gelir'), kdv_orani
- musteriler: id, ad, vkn_tckn, yurtdisi
"""


SELAMLAR = {"merhaba", "selam", "selamlar", "hi", "hello", "hey",
    "merhabalar", "iyi gunler", "iyi aksamlar", "gunaydin", "iyi geceler"}

NASILSIN = {"nasilsin", "naber", "nasil gidiyor", "iyi misin", "naptin", 
    "ne haber", "gunun nasil gecti", "gunun nasildi", "ne yapiyorsun"}

TESEKKUR = {"tesekkurler", "tesekkur ederim", "sagol", "sagolun", "thanks"}

BELIRSIZ = {"sorabilir miyim", "soru sormak istiyorum", "yardim", "yardim et",
    "yardim eder misin", "cevap ver", "soru", "sorabilir miymi",
    "baska bir sey sorabilir miyim", "sen kimsin", "kim oldugunu",
    "ne yapabilirsin", "neler yapabilirsin"}


def normalize(metin):
    metin = metin.lower().strip()
    cevirme = str.maketrans({
        "c": "c", "g": "g", "i": "i", "o": "o", "s": "s", "u": "u"
    })
    metin = metin.translate(cevirme)
    metin = re.sub(r'[^\w\s]', '', metin)
    return metin.strip()


def hizli_cevap_var_mi(soru):
    norm = normalize(soru)

    if norm in SELAMLAR:
        return ("Merhaba! Vergi ve fatura verileriniz hakkinda "
                "sorularinizi yanitlayabilirim.\n\n"
                "Ornek sorular:\n"
                "- Toplam ne kadar harcadim?\n"
                "- Kac musterim var?\n"
                "- En son eklenen gider neydi?")

    if norm in NASILSIN:
        return "Iyiyim, tesekkurler! Verileriniz hakkinda ne ogrenmek istersiniz?"

    if norm in TESEKKUR:
        return "Rica ederim! Baska sormak istediginiz var mi?"

    if norm in BELIRSIZ or len(norm) < 3:
        return ("Tabii ki! Lutfen spesifik bir soru sorun.\n\n"
                "Ornekler:\n"
                "- Bu ay toplam ne kadar harcadim?\n"
                "- En cok hangi kategoride harciyorum?\n"
                "- Toplam KDV tutari ne kadar?")

    return None


def sql_agent_olustur():
    llm = ChatOllama(
        model="llama3.1:8b",
        temperature=0,
        base_url="http://localhost:11434",
        num_ctx=4096,
    )
    db = SQLDatabase.from_uri(DATABASE_URL)
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    agent = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=False,
        agent_type="tool-calling",
        prefix=SISTEM_PROMPT,
        max_iterations=15,
        handle_parsing_errors=True
    )
    return agent


def cevabi_temizle(cevap):
    cevap = cevap.strip()

    gecis_ifadeleri = [
        "Now, I can answer your question.",
        "Now I can answer your question.",
        "Final Answer:",
        "Final Answer",
        "Answer:",
        "Cevap:",
    ]
    for ifade in gecis_ifadeleri:
        if ifade in cevap:
            cevap = cevap.split(ifade)[-1].strip(": \n")
            break

    if len(cevap) > 300:
        paragraflar = [p.strip() for p in cevap.split("\n\n") if p.strip()]
        duz_paragraflar = [
            p for p in paragraflar
            if not p.startswith("*")
            and not p.startswith("-")
            and not p.startswith("#")
            and not p.startswith("The table")
            and "(date)" not in p
            and "(vendor)" not in p
        ]
        if duz_paragraflar:
            cevap = duz_paragraflar[-1]

    return cevap.strip()


def soru_sor(soru):
    hizli = hizli_cevap_var_mi(soru)
    if hizli:
        return hizli

    try:
        agent = sql_agent_olustur()
        result = agent.invoke({"input": soru})
        cevap = result.get("output", "")
        cevap = cevabi_temizle(cevap)

        if not cevap or len(cevap.strip()) < 5:
            return ("Sorunuzu tam anlayamadim.\n\n"
                    "Lutfen daha spesifik bir soru sorun.\n"
                    "Ornek: 'Toplam ne kadar harcadim?'")

        return cevap
    except Exception as e:
        return f"Bir hata olustu: {str(e)}"
