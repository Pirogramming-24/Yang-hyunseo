from transformers import (
    pipeline,
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
)


# ===============================
# 1️⃣ Translation (NLLB)
# ===============================
MODEL_NAME = "facebook/nllb-200-distilled-600M"

_nllb_tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME,
    use_fast=False,   # 🔥 중요
)

_nllb_model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_NAME
)

LANG_CODE = {
    "ko": "kor_Hang",
    "en": "eng_Latn",
    "ja": "jpn_Jpan",
}

def run_translate(text, target_lang="en"):
    tgt_lang = LANG_CODE.get(target_lang, "eng_Latn")

    # source language 지정
    _nllb_tokenizer.src_lang = "kor_Hang"

    inputs = _nllb_tokenizer(
        text,
        return_tensors="pt"
    )

    forced_bos_token_id = _nllb_tokenizer.convert_tokens_to_ids(tgt_lang)

    outputs = _nllb_model.generate(
        **inputs,
        forced_bos_token_id=forced_bos_token_id,
        max_new_tokens=200,
    )

    return _nllb_tokenizer.batch_decode(
        outputs,
        skip_special_tokens=True
    )[0]




# ===============================
# 2️⃣ Sentiment Analysis
# ===============================
_sentiment = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

def run_sentiment(text):
    result = _sentiment(text)[0]
    return f'{result["label"]} ({result["score"]:.2f})'


# ===============================
# 3️⃣ Text Generation (distilgpt2)
# ===============================

MODEL_NAME = "distilgpt2"

_generator = None
_tokenizer = None


def get_generator():
    global _generator, _tokenizer

    if _generator is None:
        try:
            _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

            _generator = pipeline(
                "text-generation",
                model=MODEL_NAME,
                tokenizer=_tokenizer,
                device=-1,        # ✅ CPU 고정
            )

        except Exception as e:
            # ❗ 중간 실패 시 meta tensor 방지
            _generator = None
            _tokenizer = None
            raise e

    return _generator

    return _generator


def run_generate(prompt):
    generator = get_generator()

    result = generator(
        prompt,
        max_new_tokens=80,     # 더 줄임 (안정성 ↑)
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
        repetition_penalty=1.1,
        pad_token_id=_tokenizer.eos_token_id,
        eos_token_id=_tokenizer.eos_token_id,
    )

    return result[0]["generated_text"]



# ===============================
# 4️⃣ Dispatcher
# ===============================
def run_ai(model_type, input_text):
    if model_type == "translate":
        return run_translate(input_text)

    if model_type == "sentiment":
        return run_sentiment(input_text)

    if model_type == "generate":
        return run_generate(input_text)

    raise ValueError(f"Unknown task type: {model_type}")
