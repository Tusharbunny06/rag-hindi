# Test query log

- Generated: 2026-10-22 14:55
- Document: `Agni_Ki_Udaan_Adhyayan_Sahayika_Hindi.pdf` · chunks indexed: 95
- Retrieval: `BAAI/bge-m3` embeddings · ChromaDB (cosine) · top-k = 4
- Answer generator: `hf:Qwen/Qwen2.5-1.5B-Instruct (cpu, bfloat16)`
- Faithfulness judge: `groq:openai/gpt-oss-120b` (a different model from the generator)
- Every answer and citation below was produced by the pipeline. page / section / chunk_id come from the metadata stored in ChromaDB. The *Reference* column is hand-written ground truth used only for scoring.

## Scorecard

| Metric | Result | Target / note |
|---|---|---|
| Answer accuracy (gold keywords present) | 5/6 (83%) | |
| Citation accuracy (a cited chunk is on a gold page) | 6/6 (100%) | |
| Faithfulness (claims supported by retrieved passages, LLM judge) | 0.917 | ≥ 0.85 |
| Numbers in answer found in retrieved context | 6/6 (100%) | automatic check |
| Retrieval latency, median (query embedding + vector search) | 396 ms | |
| LLM time to first token, median | 131,525 ms | |
| **End-to-end TTFT, median / max** | **131,918 / 260,755 ms** | < 420 ms (see README §Latency) |

## Answers

| # | Lang | Query | System answer | Source (citation) | Reference | ✓ | Faithf. | TTFT ms |
|---|---|---|---|---|---|---|---|---|
| 1 | hi | SLV-III ने किस उपग्रह को कक्षा में स्थापित किया और किस वर्ष? | SLV-III ने रोहिणी उपग्रह को कक्षा में स्थापित किया, जिससे भारत उन थोड़े-से देशों के समूह में आ गया जो अपने रॉकेटों से उपग्रह प्रक्षेपित कर सकते थे। 1980 में | page: 8 · section: "इसरो के वर्ष और SLV-III" · chunk_id: 19 · score: 0.68 | रोहिणी उपग्रह; 1980 | ✅ | 1.00 | 100,196 |
| 2 | hi | कलाम को भारत रत्न किस वर्ष प्राप्त हुआ? | वर्ष: 1997 | page: 16 · section: "पुरस्कार एवं सम्मान" · chunk_id: 50 · score: 0.57<br>page: 16 · section: "पुरस्कार एवं सम्मान" · chunk_id: 51 · score: 0.45 | 1997 | ✅ | 1.00 | 181,302 |
| 3 | hi | पोखरण-II में कलाम की क्या भूमिका थी? | कलाम, जो उस समय रक्षा मंत्री के वैज्ञानिक सलाहकार तथा डीआरडीओ के प्रमुख के रूप में सेवारत थे, ने परमाणु ऊर्जा विभाग के वैज्ञानिकों के साथ मिलकर एक केंद्रीय संगठनात्मक भूमिका न | page: 10 · section: "पोखरण-II: 1998 के परमाणु परीक्षण" · chunk_id: 27 · score: 0.64 | केंद्रीय संगठनात्मक भूमिका — रक्षा मंत्री के वैज्ञानिक सलाहकार और डीआरडीओ प्रमुख के रूप में, परमाणु ऊर्जा विभाग के वैज्ञानिकों के साथ मिलकर | ✅ | 1.00 | 260,755 |
| 4 | en | Which institution did Kalam attend to study aeronautical engineering? | Chennai's Madras Institute of Technology (EAMT) | page: 6 · section: "कॉलेज के वर्ष और उड़ान का आकर्षण" · chunk_id: 12 · score: 0.57 | Madras Institute of Technology (MIT), Chennai | ✅ | 1.00 | 150,128 |
| 5 | en | Who co-wrote the autobiography, and in what year was it published? | Arun Tivari wrote the autobiography along with A.P.J. Abdul Kalam, which was published in 1999. | page: 3 · section: "ए.पी.जे. अब्दुल कलाम कौन थे?" · chunk_id: 4 · score: 0.53<br>page: 17 · section: "जीवन-रेखा (टाइमलाइन)" · chunk_id: 63 · score: 0.45 | Arun Tiwari (अरुण तिवारी); 1999 | ✅ | 1.00 | 113,707 |
| 6 | en | How and where did Kalam die in 2015? | Kalam died on July 27, 2015, while lecturing at Shilang's Indian National Development Society. | page: 15 · section: "अंतिम क्षण तक शिक्षक (2007–2015)" · chunk_id: 46 · score: 0.55<br>page: 17 · section: "जीवन-रेखा (टाइमलाइन)" · chunk_id: 66 · score: 0.44 | 27 July 2015 in Shillong (IIM Shillong): he collapsed while lecturing to students and died shortly after, aged 83 | ❌ | 0.50 | 107,830 |

## Full output per query

### 1. (hi)

```text
Query   : SLV-III ने किस उपग्रह को कक्षा में स्थापित किया और किस वर्ष?
Answer  : SLV-III ने रोहिणी उपग्रह को कक्षा में स्थापित किया, जिससे भारत उन थोड़े-से देशों के समूह में आ गया जो अपने रॉकेटों से उपग्रह प्रक्षेपित कर सकते थे। 1980 में
Source  : page: 8 · section: "इसरो के वर्ष और SLV-III" · chunk_id: 19 · score: 0.68
Latency : retrieval 436 ms + LLM first token 99,761 ms = end-to-end TTFT 100,196 ms (LLM complete after 227,574 ms)  [hf:Qwen/Qwen2.5-1.5B-Instruct (cpu, bfloat16)]
Retrieved context (rank · page · chunk_id · score):
  *1. p8 · #19 · 0.68 · जुलाई 1980 में, SLV-III ने रोहिणी उपग्रह को सफलतापूर्वक कक्षा में स्थापित किया, जिससे भारत
   2. p20 · #75 · 0.65 · रोहिणी: 1980 में SLV-III द्वारा कक्षा में स्थापित उपग्रह।
   3. p17 · #59 · 0.64 · 1980: SLV-III ने रोहिणी उपग्रह को कक्षा में स्थापित किया।
   4. p8 · #17 · 0.62 · इसरो में कलाम उपग्रह प्रक्षेपण यान — SLV-III — के निर्माण की परियोजना का नेतृत्व करने तक प
  judge: supported   · SLV-III ने रोहिणी उपग्रह को कक्षा में स्थापित किया।
  judge: supported   · इससे भारत उन थोड़े-से देशों के समूह में आ गया जो अपने रॉकेटों से उपग्रह प्रक्षेपित कर सकते थे।
  judge: supported   · यह घटना 1980 में हुई।
```

### 2. (hi)

```text
Query   : कलाम को भारत रत्न किस वर्ष प्राप्त हुआ?
Answer  : वर्ष: 1997
Source  : page: 16 · section: "पुरस्कार एवं सम्मान" · chunk_id: 50 · score: 0.57
          page: 16 · section: "पुरस्कार एवं सम्मान" · chunk_id: 51 · score: 0.45
Note    : citation inferred (lexical): the model gave no [n] marker
Latency : retrieval 409 ms + LLM first token 180,894 ms = end-to-end TTFT 181,303 ms (LLM complete after 184,097 ms)  [hf:Qwen/Qwen2.5-1.5B-Instruct (cpu, bfloat16)]
Retrieved context (rank · page · chunk_id · score):
   1. p20 · #79 · 0.72 · भारत रत्न: भारत का सर्वोच्च नागरिक सम्मान, 1997 में कलाम को प्रदान।
   2. p16 · #47 · 0.59 · कलाम को भारत के सर्वोच्च नागरिक सम्मान तथा अनेक अंतरराष्ट्रीय मान्यताएँ प्राप्त हुईं। कुछ 
   3. p3 · #3 · 0.57 · अवुल पाकिर जैनुलाब्दीन अब्दुल कलाम (1931–2015) एक भारतीय एयरोस्पेस वैज्ञानिक तथा भारत के ग
  *4. p16 · #50 · 0.57 · वर्ष: 1997; सम्मान: भारत रत्न; टिप्पणी: भारत का सर्वोच्च नागरिक सम्मान।
   5. p16 · #49 · 0.50 · वर्ष: 1990; सम्मान: पद्म विभूषण; टिप्पणी: भारत का दूसरा सर्वोच्च नागरिक पुरस्कार।
   6. p16 · #48 · 0.48 · वर्ष: 1981; सम्मान: पद्म भूषण; टिप्पणी: विज्ञान एवं इंजीनियरिंग में योगदान के लिए।
  *7. p16 · #51 · 0.45 · वर्ष: 1997; सम्मान: राष्ट्रीय एकता के लिए इंदिरा गांधी पुरस्कार
   8. p16 · #52 · 0.32 · वर्ष: विभिन्न; सम्मान: मानद डॉक्टरेट; टिप्पणी: विश्व भर के चालीस से अधिक विश्वविद्यालयों स
  judge: supported   · कलाम को भारत रत्न 1997 में प्राप्त हुआ
```

### 3. (hi)

```text
Query   : पोखरण-II में कलाम की क्या भूमिका थी?
Answer  : कलाम, जो उस समय रक्षा मंत्री के वैज्ञानिक सलाहकार तथा डीआरडीओ के प्रमुख के रूप में सेवारत थे, ने परमाणु ऊर्जा विभाग के वैज्ञानिकों के साथ मिलकर एक केंद्रीय संगठनात्मक भूमिका न
Source  : page: 10 · section: "पोखरण-II: 1998 के परमाणु परीक्षण" · chunk_id: 27 · score: 0.64
Note    : citation inferred (lexical): the model gave no [n] marker
Latency : retrieval 383 ms + LLM first token 260,372 ms = end-to-end TTFT 260,755 ms (LLM complete after 379,466 ms)  [hf:Qwen/Qwen2.5-1.5B-Instruct (cpu, bfloat16)]
Retrieved context (rank · page · chunk_id · score):
  *1. p10 · #27 · 0.64 · मई 1998 में, भारत ने राजस्थान के पोखरण में भूमिगत परमाणु परीक्षणों की एक शृंखला की, जिसे प
   2. p10 · #28 · 0.56 · ये परीक्षण कड़ी गोपनीयता और सटीक समन्वय के साथ किए गए, और इन्होंने भारत की सामरिक स्थिति म
   3. p3 · #3 · 0.48 · अवुल पाकिर जैनुलाब्दीन अब्दुल कलाम (1931–2015) एक भारतीय एयरोस्पेस वैज्ञानिक तथा भारत के ग
   4. p14 · #44 · 0.48 · कलाम इस पद पर एक वैज्ञानिक की आदतें लेकर आए: जिज्ञासा, सीधी बात, और बहानों के प्रति अधीरता
  judge: supported   · कलाम उस समय रक्षा मंत्री के वैज्ञानिक सलाहकार थे।
  judge: supported   · कलाम उस समय डीआरडीओ के प्रमुख के रूप में सेवारत थे।
  judge: supported   · कलाम ने परमाणु ऊर्जा विभाग के वैज्ञानिकों के साथ मिलकर एक केंद्रीय संगठनात्मक भूमिका निभाई।
```

### 4. (en)

```text
Query   : Which institution did Kalam attend to study aeronautical engineering?
Answer  : Chennai's Madras Institute of Technology (EAMT)
Source  : page: 6 · section: "कॉलेज के वर्ष और उड़ान का आकर्षण" · chunk_id: 12 · score: 0.57
Note    : citation inferred (top-1): the model gave no [n] marker
Latency : retrieval 410 ms + LLM first token 149,718 ms = end-to-end TTFT 150,128 ms (LLM complete after 157,121 ms)  [hf:Qwen/Qwen2.5-1.5B-Instruct (cpu, bfloat16)]
Retrieved context (rank · page · chunk_id · score):
  *1. p6 · #12 · 0.57 · उन्होंने वैमानिकी इंजीनियरिंग पढ़ने के लिए चेन्नई के मद्रास इंस्टीट्यूट ऑफ टेक्नोलॉजी (एमआ
   2. p6 · #11 · 0.56 · स्कूल के बाद, कलाम ने तिरुचिरापल्ली के सेंट जोसेफ कॉलेज में भौतिकी पढ़ी और 1950 के दशक के 
   3. p7 · #14 · 0.50 · कलाम ने अपना व्यावसायिक जीवन भारत के रक्षा प्रतिष्ठान के अंग, तकनीकी विकास एवं उत्पादन निद
   4. p3 · #3 · 0.48 · अवुल पाकिर जैनुलाब्दीन अब्दुल कलाम (1931–2015) एक भारतीय एयरोस्पेस वैज्ञानिक तथा भारत के ग
  judge: supported   · Kalam attended Madras Institute of Technology in Chennai to study aeronautical engineering.
```

### 5. (en)

```text
Query   : Who co-wrote the autobiography, and in what year was it published?
Answer  : Arun Tivari wrote the autobiography along with A.P.J. Abdul Kalam, which was published in 1999.
Source  : page: 3 · section: "ए.पी.जे. अब्दुल कलाम कौन थे?" · chunk_id: 4 · score: 0.53
          page: 17 · section: "जीवन-रेखा (टाइमलाइन)" · chunk_id: 63 · score: 0.45
Latency : retrieval 375 ms + LLM first token 113,332 ms = end-to-end TTFT 113,707 ms (LLM complete after 133,638 ms)  [hf:Qwen/Qwen2.5-1.5B-Instruct (cpu, bfloat16)]
Retrieved context (rank · page · chunk_id · score):
  *1. p3 · #4 · 0.53 · अग्नि की उड़ान, जो 1999 में प्रकाशित हुई और वैज्ञानिक अरुण तिवारी के साथ मिलकर लिखी गई, उन
   2. p1 · #0 · 0.49 · अग्नि की उड़ान ए.पी.जे. अब्दुल कलाम का जीवन, कार्य और विचार अवुल पाकिर जैनुलाब्दीन अब्दुल 
   3. p22 · #91 · 0.48 · आत्मकथा: अग्नि की उड़ान (1999), अरुण तिवारी के साथ
  *4. p17 · #63 · 0.45 · 1999: अग्नि की उड़ान प्रकाशित (अरुण तिवारी के साथ)।
  judge: supported   · Arun Tivari co-wrote the autobiography with A.P.J. Abdul Kalam.
  judge: supported   · The autobiography was published in 1999.
```

### 6. (en)

```text
Query   : How and where did Kalam die in 2015?
Answer  : Kalam died on July 27, 2015, while lecturing at Shilang's Indian National Development Society.
Source  : page: 15 · section: "अंतिम क्षण तक शिक्षक (2007–2015)" · chunk_id: 46 · score: 0.55
          page: 17 · section: "जीवन-रेखा (टाइमलाइन)" · chunk_id: 66 · score: 0.44
Note    : citation inferred (lexical): the model gave no [n] marker
Latency : retrieval 336 ms + LLM first token 107,493 ms = end-to-end TTFT 107,829 ms (LLM complete after 124,818 ms)  [hf:Qwen/Qwen2.5-1.5B-Instruct (cpu, bfloat16)]
Retrieved context (rank · page · chunk_id · score):
  *1. p15 · #46 · 0.55 · 27 जुलाई 2015 को, कलाम शिलांग के भारतीय प्रबंधन संस्थान में विद्यार्थियों को व्याख्यान देत
   2. p3 · #3 · 0.47 · अवुल पाकिर जैनुलाब्दीन अब्दुल कलाम (1931–2015) एक भारतीय एयरोस्पेस वैज्ञानिक तथा भारत के ग
  *3. p17 · #66 · 0.44 · 2015: 27 जुलाई को शिलांग में विद्यार्थियों को व्याख्यान देते हुए निधन।
   4. p4 · #5 · 0.42 · कलाम का जन्म 15 अक्टूबर 1931 को तमिलनाडु के दक्षिण-पूर्वी तट के निकट पम्बन द्वीप पर स्थित 
  judge: supported   · Kalam died on July 27, 2015.
  judge: UNSUPPORTED · He died while lecturing at Shilang's Indian National Development Society.
```
