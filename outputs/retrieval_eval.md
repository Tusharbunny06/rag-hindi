# Retrieval evaluation

Embedding model: `BAAI/bge-m3 (float32)` · indexed chunks: 95 · filter: `answerable=True` · queries: 20 (8 Hindi, 12 English)

**Evidence hit@k** = a top-k chunk contains the answer facts. **Page hit@k** = a top-k chunk is from a page holding the answer.

| Query set | n | Evidence hit@1 | @3 | @5 | MRR | Page hit@1 | @3 | @5 |
|---|---|---|---|---|---|---|---|---|
| Required 6 (all) | 6 | 100% | 100% | 100% | 1.00 | 100% | 100% | 100% |
| All queries | 20 | 95% | 95% | 100% | 0.96 | 100% | 100% | 100% |
| Hindi queries | 8 | 88% | 88% | 100% | 0.91 | 100% | 100% | 100% |
| English queries (cross-lingual EN→HI) | 12 | 100% | 100% | 100% | 1.00 | 100% | 100% | 100% |

## Per query

| # | Lang | Query | Evidence rank | Page rank | Top-1 (page · chunk · score) |
|---|---|---|---|---|---|
| 1 | hi | SLV-III ने किस उपग्रह को कक्षा में स्थापित किया और किस वर्ष? | 1 | 1 | p8 · #19 · 0.68 |
| 2 | hi | कलाम को भारत रत्न किस वर्ष प्राप्त हुआ? | 1 | 1 | p20 · #79 · 0.72 |
| 3 | hi | पोखरण-II में कलाम की क्या भूमिका थी? | 1 | 1 | p10 · #27 · 0.64 |
| 4 | en | Which institution did Kalam attend to study aeronautical engineering? | 1 | 1 | p6 · #12 · 0.57 |
| 5 | en | Who co-wrote the autobiography, and in what year was it published? | 1 | 1 | p3 · #4 · 0.53 |
| 6 | en | How and where did Kalam die in 2015? | 1 | 1 | p15 · #46 · 0.55 |
| 7 | en | Which satellite did SLV-III put into orbit, and in which year? | 1 | 1 | p8 · #19 · 0.65 |
| 8 | en | In which year was Kalam awarded the Bharat Ratna? | 1 | 1 | p20 · #79 · 0.50 |
| 9 | en | What role did Kalam play in Pokhran-II? | 1 | 1 | p10 · #27 · 0.51 |
| 10 | hi | कलाम ने वैमानिकी इंजीनियरिंग किस संस्थान से पढ़ी? | 1 | 1 | p6 · #12 · 0.70 |
| 11 | hi | अग्नि की उड़ान किसके साथ मिलकर लिखी गई और कब प्रकाशित हुई? | 1 | 1 | p3 · #4 · 0.60 |
| 12 | hi | कलाम का निधन कहाँ और कैसे हुआ? | 1 | 1 | p15 · #46 · 0.63 |
| 13 | en | What are the names of the missiles developed under the IGMDP and what do the names mean? | — | 1 | p9 · #20 · 0.65 |
| 14 | en | Why did Kalam not become a fighter pilot? | 1 | 1 | p6 · #13 · 0.50 |
| 15 | en | How did Satish Dhawan handle the 1979 launch failure? | 1 | 1 | p8 · #18 · 0.58 |
| 16 | hi | कलाम को "जनता के राष्ट्रपति" क्यों कहा गया? | 1 | 1 | p14 · #43 · 0.71 |
| 17 | en | Who was Vikram Sarabhai? | 1 | 1 | p7 · #15 · 0.48 |
| 18 | en | When and where was Kalam born? | 1 | 1 | p4 · #5 · 0.54 |
| 19 | hi | कलाम ने बचपन में अख़बार क्यों बाँटे? | 4 | 1 | p4 · #5 · 0.60 |
| 20 | en | Who helped Kalam pay his college fees? | 1 | 1 | p6 · #12 · 0.51 |

## Calibrating the 'not found' threshold

Top-1 score of the 20 answerable queries: min 0.48, mean 0.59.

| Unanswerable query | Top-1 score | Top-1 chunk |
|---|---|---|
| What is the population of Tokyo? | 0.37 | p17 · #54 |
| Who won the 2018 FIFA World Cup? | 0.43 | p3 · #3 |
| पाइथन प्रोग्रामिंग भाषा किसने बनाई? | 0.39 | p9 · #20 |

Configured `MIN_SCORE` = 0.3. Scores are only a coarse first filter: the LLM is additionally instructed to answer `NOT_FOUND` when the retrieved passages do not contain the answer.
