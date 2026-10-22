# Test query log

- Generated: 2026-10-22 14:29
- Document: `Agni_Ki_Udaan_Adhyayan_Sahayika_Hindi.pdf` · chunks indexed: 95
- Retrieval: `BAAI/bge-m3` embeddings · ChromaDB (cosine) · top-k = 4
- Answer generator: `groq:qwen/qwen3.8-27b`
- Faithfulness judge: `groq:openai/gpt-oss-120b` (a different model from the generator)
- Every answer and citation below was produced by the pipeline. page / section / chunk_id come from the metadata stored in ChromaDB. The *Reference* column is hand-written ground truth used only for scoring.

## Scorecard

| Metric | Result | Target / note |
|---|---|---|
| Answer accuracy (gold keywords present) | 20/20 (100%) | |
| Citation accuracy (a cited chunk is on a gold page) | 20/20 (100%) | |
| Faithfulness (claims supported by retrieved passages, LLM judge) | 1.0 | ≥ 0.85 |
| Numbers in answer found in retrieved context | 20/20 (100%) | automatic check |
| Out-of-scope questions correctly refused | 3/3 (100%) | |
| Retrieval latency, median (query embedding + vector search) | 396 ms | |
| LLM time to first token, median | 691 ms | |
| **End-to-end TTFT, median / max** | **1,067 / 2,151 ms** | < 420 ms (see README §4) |

## Answers

| # | Lang | Query | System answer | Source (citation) | Reference | ✓ | Faithf. | TTFT ms |
|---|---|---|---|---|---|---|---|---|
| 1 | hi | SLV-III ने किस उपग्रह को कक्षा में स्थापित किया और किस वर्ष? | SLV-III ने 1980 में रोहिणी उपग्रह को कक्षा में स्थापित किया। | page: 8 · section: "इसरो के वर्ष और SLV-III" · chunk_id: 19 · score: 0.68<br>page: 20 · section: "संस्थाओं एवं शब्दों की शब्दावली" · chunk_id: 75 · score: 0.65<br>page: 17 · section: "जीवन-रेखा (टाइमलाइन)" · chunk_id: 59 · score: 0.64 | रोहिणी उपग्रह; 1980 | ✅ | 1.00 | 722 |
| 2 | hi | कलाम को भारत रत्न किस वर्ष प्राप्त हुआ? | कलाम को भारत रत्न 1997 में प्राप्त हुआ। | page: 20 · section: "संस्थाओं एवं शब्दों की शब्दावली" · chunk_id: 79 · score: 0.72<br>page: 16 · section: "पुरस्कार एवं सम्मान" · chunk_id: 50 · score: 0.57 | 1997 | ✅ | 1.00 | 1,018 |
| 3 | hi | पोखरण-II में कलाम की क्या भूमिका थी? | कलाम ने उस समय रक्षा मंत्री के वैज्ञानिक सलाहकार तथा डीआरडीओ के प्रमुख के रूप में परमाणु ऊर्जा विभाग के वैज्ञानिकों के साथ मिलकर एक केंद्रीय संगठनात्मक भूमिका निभाई। | page: 10 · section: "पोखरण-II: 1998 के परमाणु परीक्षण" · chunk_id: 27 · score: 0.64 | केंद्रीय संगठनात्मक भूमिका — रक्षा मंत्री के वैज्ञानिक सलाहकार और डीआरडीओ प्रमुख के रूप में, परमाणु ऊर्जा विभाग के वैज्ञानिकों के साथ मिलकर | ✅ | 1.00 | 1,057 |
| 4 | en | Which institution did Kalam attend to study aeronautical engineering? | Kalam attended the Madras Institute of Technology (MIT) in Chennai to study aeronautical engineering. | page: 6 · section: "कॉलेज के वर्ष और उड़ान का आकर्षण" · chunk_id: 12 · score: 0.57 | Madras Institute of Technology (MIT), Chennai | ✅ | 1.00 | 1,184 |
| 5 | en | Who co-wrote the autobiography, and in what year was it published? | The autobiography was co-written by Arun Tiwari and published in 1999. | page: 3 · section: "ए.पी.जे. अब्दुल कलाम कौन थे?" · chunk_id: 4 · score: 0.53<br>page: 22 · section: "त्वरित तथ्य-सारांश" · chunk_id: 91 · score: 0.48<br>page: 17 · section: "जीवन-रेखा (टाइमलाइन)" · chunk_id: 63 · score: 0.45 | Arun Tiwari (अरुण तिवारी); 1999 | ✅ | 1.00 | 1,009 |
| 6 | en | How and where did Kalam die in 2015? | Kalam died on July 27, 2015, in Shillong after collapsing while delivering a lecture to students at the Indian Institute of Management. | page: 15 · section: "अंतिम क्षण तक शिक्षक (2007–2015)" · chunk_id: 46 · score: 0.55<br>page: 17 · section: "जीवन-रेखा (टाइमलाइन)" · chunk_id: 66 · score: 0.44 | 27 July 2015 in Shillong (IIM Shillong): he collapsed while lecturing to students and died shortly after, aged 83 | ✅ | 1.00 | 974 |
| 7 | en | Which satellite did SLV-III put into orbit, and in which year? | SLV-III put the Rohini satellite into orbit in 1980. | page: 8 · section: "इसरो के वर्ष और SLV-III" · chunk_id: 19 · score: 0.65<br>page: 20 · section: "संस्थाओं एवं शब्दों की शब्दावली" · chunk_id: 75 · score: 0.57 | Rohini; 1980 | ✅ | 1.00 | 1,060 |
| 8 | en | In which year was Kalam awarded the Bharat Ratna? | Kalam was awarded the Bharat Ratna in 1997. | page: 20 · section: "संस्थाओं एवं शब्दों की शब्दावली" · chunk_id: 79 · score: 0.50<br>page: 16 · section: "पुरस्कार एवं सम्मान" · chunk_id: 50 · score: 0.43 | 1997 | ✅ | 1.00 | 1,112 |
| 9 | en | What role did Kalam play in Pokhran-II? | Kalam played a central organizational role in Pokhran-II as the Scientific Adviser to the Defence Minister and the head of DRDO, working alongside scientists from the Department of Atomic Energy. | page: 10 · section: "पोखरण-II: 1998 के परमाणु परीक्षण" · chunk_id: 27 · score: 0.51 | A central organisational role | ✅ | 1.00 | 1,008 |
| 10 | hi | कलाम ने वैमानिकी इंजीनियरिंग किस संस्थान से पढ़ी? | कलाम ने वैमानिकी इंजीनियरिंग चेन्नई के मद्रास इंस्टीट्यूट ऑफ टेक्नोलॉजी (एमआईटी) से पढ़ी। | page: 6 · section: "कॉलेज के वर्ष और उड़ान का आकर्षण" · chunk_id: 12 · score: 0.70<br>page: 20 · section: "संस्थाओं एवं शब्दों की शब्दावली" · chunk_id: 77 · score: 0.66 | एमआईटी, चेन्नई | ✅ | 1.00 | 1,165 |
| 11 | hi | अग्नि की उड़ान किसके साथ मिलकर लिखी गई और कब प्रकाशित हुई? | अग्नि की उड़ान वैज्ञानिक अरुण तिवारी के साथ मिलकर लिखी गई थी और इसका प्रकाशन 1999 में हुआ था। | page: 3 · section: "ए.पी.जे. अब्दुल कलाम कौन थे?" · chunk_id: 4 · score: 0.60<br>page: 17 · section: "जीवन-रेखा (टाइमलाइन)" · chunk_id: 63 · score: 0.58<br>page: 22 · section: "त्वरित तथ्य-सारांश" · chunk_id: 91 · score: 0.57 | अरुण तिवारी के साथ; 1999 | ✅ | 1.00 | 1,756 |
| 12 | hi | कलाम का निधन कहाँ और कैसे हुआ? | कलाम का निधन 27 जुलाई 2015 को शिलांग के भारतीय प्रबंधन संस्थान में विद्यार्थियों को व्याख्यान देते समय गिरने के कुछ ही देर बाद हुआ। | page: 15 · section: "अंतिम क्षण तक शिक्षक (2007–2015)" · chunk_id: 46 · score: 0.63 | 27 जुलाई 2015 को शिलांग में, व्याख्यान देते समय गिरने के बाद | ✅ | 1.00 | 1,004 |
| 13 | en | What are the names of the missiles developed under the IGMDP and what do the names mean? | The missiles developed under the IGMDP are Nag (meaning "Nag/Cobra"), Prithvi (meaning "Earth"), Agni (meaning "Fire"), Trishul (meaning "Trishul"), and Akash (meaning "Sky"). | page: 9 · section: "निर्देशित मिसाइल कार्यक्रम" · chunk_id: 25 · score: 0.44<br>page: 9 · section: "निर्देशित मिसाइल कार्यक्रम" · chunk_id: 21 · score: 0.42<br>page: 9 · section: "निर्देशित मिसाइल कार्यक्रम" · chunk_id: 22 · score: 0.41<br>page: 9 · section: "निर्देशित मिसाइल कार्यक्रम" · chunk_id: 23 · score: 0.41<br>page: 9 · section: "निर्देशित मिसाइल कार्यक्रम" · chunk_id: 24 · score: 0.40 | Prithvi, Agni, Trishul, Akash, Nag (see page 9 table) | ✅ | 1.00 | 1,350 |
| 14 | en | Why did Kalam not become a fighter pilot? | Kalam did not become a fighter pilot because he narrowly missed selection for the Indian Air Force, finishing in ninth place when only eight positions were available. | page: 6 · section: "कॉलेज के वर्ष और उड़ान का आकर्षण" · chunk_id: 13 · score: 0.50 | He placed 9th for the Air Force when only 8 places were available | ✅ | 1.00 | 1,210 |
| 15 | en | How did Satish Dhawan handle the 1979 launch failure? | Satish Dhawan publicly took responsibility for the 1979 launch failure and protected his team. | page: 8 · section: "इसरो के वर्ष और SLV-III" · chunk_id: 18 · score: 0.58<br>page: 12 · section: "गुरु एवं शिक्षक" · chunk_id: 38 · score: 0.46 | He publicly took responsibility for the failure and protected his team | ✅ | 1.00 | 2,151 |
| 16 | hi | कलाम को "जनता के राष्ट्रपति" क्यों कहा गया? | कलाम को उनकी गर्मजोशी, सुलभता और आम नागरिकों, विशेषकर विद्यार्थियों के साथ अथक संवाद के कारण "जनता के राष्ट्रपति" कहा गया। | page: 14 · section: "जनता के राष्ट्रपति (2002–2007)" · chunk_id: 43 · score: 0.71 | अपनी गर्मजोशी, सुलभता और आम नागरिकों व विद्यार्थियों से अथक संवाद के कारण | ✅ | 1.00 | 942 |
| 17 | en | Who was Vikram Sarabhai? | Vikram Sarabhai was a visionary physicist widely regarded as the father of India's space program. | page: 7 · section: "वैज्ञानिक करियर के पहले कदम" · chunk_id: 15 · score: 0.48<br>page: 12 · section: "गुरु एवं शिक्षक" · chunk_id: 37 · score: 0.42 | Visionary physicist, father of India's space programme; Kalam's early mentor | ✅ | 1.00 | 1,067 |
| 18 | en | When and where was Kalam born? | Kalam was born on October 15, 1931, in Rameswaram, Tamil Nadu. | page: 4 · section: "रामेश्वरम में बचपन" · chunk_id: 5 · score: 0.54<br>page: 17 · section: "जीवन-रेखा (टाइमलाइन)" · chunk_id: 54 · score: 0.43 | 15 October 1931, Rameswaram, Tamil Nadu | ✅ | 1.00 | 1,346 |
| 19 | hi | कलाम ने बचपन में अख़बार क्यों बाँटे? | द्वितीय विश्वयुद्ध के दौरान रेल सेवाओं में बाधा के कारण कलाम ने चलती ट्रेन से गिराए गए अख़बार एकत्रित करके बाँटे, जिससे उन्हें अपना पहला स्वयं कमाया धन मिला। | page: 4 · section: "रामेश्वरम में बचपन" · chunk_id: 7 · score: 0.58 | परिवार की आय बढ़ाने / परिवार की मदद के लिए | ✅ | 1.00 | 1,190 |
| 20 | en | Who helped Kalam pay his college fees? | His sister helped pay his college fees by pawning her jewelry. | page: 6 · section: "कॉलेज के वर्ष और उड़ान का आकर्षण" · chunk_id: 12 · score: 0.51 | His sister, who pawned her jewellery | ✅ | 1.00 | 1,170 |
| 21 | en | What is the population of Tokyo? | The document does not contain an answer to this question. | — | out of scope: should abstain | ✅ | — | 1,019 |
| 22 | en | Who won the 2018 FIFA World Cup? | The document does not contain an answer to this question. | — | out of scope: should abstain | ✅ | — | 955 |
| 23 | hi | पाइथन प्रोग्रामिंग भाषा किसने बनाई? | दस्तावेज़ में इस प्रश्न का उत्तर उपलब्ध नहीं है। | — | out of scope: should abstain | ✅ | — | 1,816 |

## Full output per query

### 1. (hi)

```text
Query   : SLV-III ने किस उपग्रह को कक्षा में स्थापित किया और किस वर्ष?
Answer  : SLV-III ने 1980 में रोहिणी उपग्रह को कक्षा में स्थापित किया।
Source  : page: 8 · section: "इसरो के वर्ष और SLV-III" · chunk_id: 19 · score: 0.68
          page: 20 · section: "संस्थाओं एवं शब्दों की शब्दावली" · chunk_id: 75 · score: 0.65
          page: 17 · section: "जीवन-रेखा (टाइमलाइन)" · chunk_id: 59 · score: 0.64
Latency : retrieval 485 ms + LLM first token 236 ms = end-to-end TTFT 722 ms (LLM complete after 304 ms)  [groq:qwen/qwen3.8-27b]
Retrieved context (rank · page · chunk_id · score):
  *1. p8 · #19 · 0.68 · जुलाई 1980 में, SLV-III ने रोहिणी उपग्रह को सफलतापूर्वक कक्षा में स्थापित किया, जिससे भारत
  *2. p20 · #75 · 0.65 · रोहिणी: 1980 में SLV-III द्वारा कक्षा में स्थापित उपग्रह।
  *3. p17 · #59 · 0.64 · 1980: SLV-III ने रोहिणी उपग्रह को कक्षा में स्थापित किया।
   4. p8 · #17 · 0.62 · इसरो में कलाम उपग्रह प्रक्षेपण यान — SLV-III — के निर्माण की परियोजना का नेतृत्व करने तक प
  judge: supported   · SLV-III ने रोहिणी उपग्रह को कक्षा में स्थापित किया।
  judge: supported   · यह 1980 में हुआ।
```

### 2. (hi)

```text
Query   : कलाम को भारत रत्न किस वर्ष प्राप्त हुआ?
Answer  : कलाम को भारत रत्न 1997 में प्राप्त हुआ।
Source  : page: 20 · section: "संस्थाओं एवं शब्दों की शब्दावली" · chunk_id: 79 · score: 0.72
          page: 16 · section: "पुरस्कार एवं सम्मान" · chunk_id: 50 · score: 0.57
Latency : retrieval 384 ms + LLM first token 634 ms = end-to-end TTFT 1,018 ms (LLM complete after 671 ms)  [groq:qwen/qwen3.8-27b]
Retrieved context (rank · page · chunk_id · score):
  *1. p20 · #79 · 0.72 · भारत रत्न: भारत का सर्वोच्च नागरिक सम्मान, 1997 में कलाम को प्रदान।
   2. p16 · #47 · 0.59 · कलाम को भारत के सर्वोच्च नागरिक सम्मान तथा अनेक अंतरराष्ट्रीय मान्यताएँ प्राप्त हुईं। कुछ 
   3. p3 · #3 · 0.57 · अवुल पाकिर जैनुलाब्दीन अब्दुल कलाम (1931–2015) एक भारतीय एयरोस्पेस वैज्ञानिक तथा भारत के ग
  *4. p16 · #50 · 0.57 · वर्ष: 1997; सम्मान: भारत रत्न; टिप्पणी: भारत का सर्वोच्च नागरिक सम्मान।
   5. p16 · #49 · 0.50 · वर्ष: 1990; सम्मान: पद्म विभूषण; टिप्पणी: भारत का दूसरा सर्वोच्च नागरिक पुरस्कार।
   6. p16 · #48 · 0.48 · वर्ष: 1981; सम्मान: पद्म भूषण; टिप्पणी: विज्ञान एवं इंजीनियरिंग में योगदान के लिए।
   7. p16 · #51 · 0.45 · वर्ष: 1997; सम्मान: राष्ट्रीय एकता के लिए इंदिरा गांधी पुरस्कार
   8. p16 · #52 · 0.32 · वर्ष: विभिन्न; सम्मान: मानद डॉक्टरेट; टिप्पणी: विश्व भर के चालीस से अधिक विश्वविद्यालयों स
  judge: supported   · कलाम को भारत रत्न 1997 में प्राप्त हुआ।
```

### 3. (hi)

```text
Query   : पोखरण-II में कलाम की क्या भूमिका थी?
Answer  : कलाम ने उस समय रक्षा मंत्री के वैज्ञानिक सलाहकार तथा डीआरडीओ के प्रमुख के रूप में परमाणु ऊर्जा विभाग के वैज्ञानिकों के साथ मिलकर एक केंद्रीय संगठनात्मक भूमिका निभाई।
Source  : page: 10 · section: "पोखरण-II: 1998 के परमाणु परीक्षण" · chunk_id: 27 · score: 0.64
Latency : retrieval 398 ms + LLM first token 659 ms = end-to-end TTFT 1,057 ms (LLM complete after 796 ms)  [groq:qwen/qwen3.8-27b]
Retrieved context (rank · page · chunk_id · score):
  *1. p10 · #27 · 0.64 · मई 1998 में, भारत ने राजस्थान के पोखरण में भूमिगत परमाणु परीक्षणों की एक शृंखला की, जिसे प
   2. p10 · #28 · 0.56 · ये परीक्षण कड़ी गोपनीयता और सटीक समन्वय के साथ किए गए, और इन्होंने भारत की सामरिक स्थिति म
   3. p3 · #3 · 0.48 · अवुल पाकिर जैनुलाब्दीन अब्दुल कलाम (1931–2015) एक भारतीय एयरोस्पेस वैज्ञानिक तथा भारत के ग
   4. p14 · #44 · 0.48 · कलाम इस पद पर एक वैज्ञानिक की आदतें लेकर आए: जिज्ञासा, सीधी बात, और बहानों के प्रति अधीरता
  judge: supported   · कलाम उस समय रक्षा मंत्री के वैज्ञानिक सलाहकार थे।
  judge: supported   · कलाम उस समय डीआरडीओ के प्रमुख थे।
  judge: supported   · कलाम ने परमाणु ऊर्जा विभाग के वैज्ञानिकों के साथ मिलकर काम किया।
  judge: supported   · कलाम ने पोखरण-II में एक केंद्रीय संगठनात्मक भूमिका निभाई।
```

### 4. (en)

```text
Query   : Which institution did Kalam attend to study aeronautical engineering?
Answer  : Kalam attended the Madras Institute of Technology (MIT) in Chennai to study aeronautical engineering.
Source  : page: 6 · section: "कॉलेज के वर्ष और उड़ान का आकर्षण" · chunk_id: 12 · score: 0.57
Latency : retrieval 490 ms + LLM first token 694 ms = end-to-end TTFT 1,184 ms (LLM complete after 737 ms)  [groq:qwen/qwen3.8-27b]
Retrieved context (rank · page · chunk_id · score):
  *1. p6 · #12 · 0.57 · उन्होंने वैमानिकी इंजीनियरिंग पढ़ने के लिए चेन्नई के मद्रास इंस्टीट्यूट ऑफ टेक्नोलॉजी (एमआ
   2. p6 · #11 · 0.56 · स्कूल के बाद, कलाम ने तिरुचिरापल्ली के सेंट जोसेफ कॉलेज में भौतिकी पढ़ी और 1950 के दशक के 
   3. p7 · #14 · 0.50 · कलाम ने अपना व्यावसायिक जीवन भारत के रक्षा प्रतिष्ठान के अंग, तकनीकी विकास एवं उत्पादन निद
   4. p3 · #3 · 0.48 · अवुल पाकिर जैनुलाब्दीन अब्दुल कलाम (1931–2015) एक भारतीय एयरोस्पेस वैज्ञानिक तथा भारत के ग
  judge: supported   · Kalam attended the Madras Institute of Technology (MIT) in Chennai.
  judge: supported   · He attended it to study aeronautical engineering.
```

### 5. (en)

```text
Query   : Who co-wrote the autobiography, and in what year was it published?
Answer  : The autobiography was co-written by Arun Tiwari and published in 1999.
Source  : page: 3 · section: "ए.पी.जे. अब्दुल कलाम कौन थे?" · chunk_id: 4 · score: 0.53
          page: 22 · section: "त्वरित तथ्य-सारांश" · chunk_id: 91 · score: 0.48
          page: 17 · section: "जीवन-रेखा (टाइमलाइन)" · chunk_id: 63 · score: 0.45
Latency : retrieval 421 ms + LLM first token 588 ms = end-to-end TTFT 1,009 ms (LLM complete after 650 ms)  [groq:qwen/qwen3.8-27b]
Retrieved context (rank · page · chunk_id · score):
  *1. p3 · #4 · 0.53 · अग्नि की उड़ान, जो 1999 में प्रकाशित हुई और वैज्ञानिक अरुण तिवारी के साथ मिलकर लिखी गई, उन
   2. p1 · #0 · 0.49 · अग्नि की उड़ान ए.पी.जे. अब्दुल कलाम का जीवन, कार्य और विचार अवुल पाकिर जैनुलाब्दीन अब्दुल 
  *3. p22 · #91 · 0.48 · आत्मकथा: अग्नि की उड़ान (1999), अरुण तिवारी के साथ
  *4. p17 · #63 · 0.45 · 1999: अग्नि की उड़ान प्रकाशित (अरुण तिवारी के साथ)।
  judge: supported   · The autobiography was co-written by Arun Tiwari.
  judge: supported   · The autobiography was published in 1999.
```

### 6. (en)

```text
Query   : How and where did Kalam die in 2015?
Answer  : Kalam died on July 27, 2015, in Shillong after collapsing while delivering a lecture to students at the Indian Institute of Management.
Source  : page: 15 · section: "अंतिम क्षण तक शिक्षक (2007–2015)" · chunk_id: 46 · score: 0.55
          page: 17 · section: "जीवन-रेखा (टाइमलाइन)" · chunk_id: 66 · score: 0.44
Latency : retrieval 356 ms + LLM first token 617 ms = end-to-end TTFT 974 ms (LLM complete after 700 ms)  [groq:qwen/qwen3.8-27b]
Retrieved context (rank · page · chunk_id · score):
  *1. p15 · #46 · 0.55 · 27 जुलाई 2015 को, कलाम शिलांग के भारतीय प्रबंधन संस्थान में विद्यार्थियों को व्याख्यान देत
   2. p3 · #3 · 0.47 · अवुल पाकिर जैनुलाब्दीन अब्दुल कलाम (1931–2015) एक भारतीय एयरोस्पेस वैज्ञानिक तथा भारत के ग
  *3. p17 · #66 · 0.44 · 2015: 27 जुलाई को शिलांग में विद्यार्थियों को व्याख्यान देते हुए निधन।
   4. p4 · #5 · 0.42 · कलाम का जन्म 15 अक्टूबर 1931 को तमिलनाडु के दक्षिण-पूर्वी तट के निकट पम्बन द्वीप पर स्थित 
  judge: supported   · Kalam died on July 27, 2015.
  judge: supported   · Kalam died in Shillong.
  judge: supported   · Kalam died after collapsing while delivering a lecture to students.
  judge: supported   · The lecture was at the Indian Institute of Management.
```

### 7. (en)

```text
Query   : Which satellite did SLV-III put into orbit, and in which year?
Answer  : SLV-III put the Rohini satellite into orbit in 1980.
Source  : page: 8 · section: "इसरो के वर्ष और SLV-III" · chunk_id: 19 · score: 0.65
          page: 20 · section: "संस्थाओं एवं शब्दों की शब्दावली" · chunk_id: 75 · score: 0.57
Latency : retrieval 454 ms + LLM first token 606 ms = end-to-end TTFT 1,060 ms (LLM complete after 654 ms)  [groq:qwen/qwen3.8-27b]
Retrieved context (rank · page · chunk_id · score):
  *1. p8 · #19 · 0.65 · जुलाई 1980 में, SLV-III ने रोहिणी उपग्रह को सफलतापूर्वक कक्षा में स्थापित किया, जिससे भारत
   2. p20 · #73 · 0.62 · SLV-III: उपग्रह प्रक्षेपण यान — भारत का पहला स्वदेशी कक्षीय रॉकेट।
   3. p8 · #17 · 0.60 · इसरो में कलाम उपग्रह प्रक्षेपण यान — SLV-III — के निर्माण की परियोजना का नेतृत्व करने तक प
  *4. p20 · #75 · 0.57 · रोहिणी: 1980 में SLV-III द्वारा कक्षा में स्थापित उपग्रह।
  judge: supported   · SLV-III put the Rohini satellite into orbit
  judge: supported   · This happened in 1980
```

### 8. (en)

```text
Query   : In which year was Kalam awarded the Bharat Ratna?
Answer  : Kalam was awarded the Bharat Ratna in 1997.
Source  : page: 20 · section: "संस्थाओं एवं शब्दों की शब्दावली" · chunk_id: 79 · score: 0.50
          page: 16 · section: "पुरस्कार एवं सम्मान" · chunk_id: 50 · score: 0.43
Latency : retrieval 435 ms + LLM first token 677 ms = end-to-end TTFT 1,112 ms (LLM complete after 721 ms)  [groq:qwen/qwen3.8-27b]
Retrieved context (rank · page · chunk_id · score):
  *1. p20 · #79 · 0.50 · भारत रत्न: भारत का सर्वोच्च नागरिक सम्मान, 1997 में कलाम को प्रदान।
   2. p3 · #3 · 0.49 · अवुल पाकिर जैनुलाब्दीन अब्दुल कलाम (1931–2015) एक भारतीय एयरोस्पेस वैज्ञानिक तथा भारत के ग
   3. p16 · #47 · 0.44 · कलाम को भारत के सर्वोच्च नागरिक सम्मान तथा अनेक अंतरराष्ट्रीय मान्यताएँ प्राप्त हुईं। कुछ 
   4. p16 · #49 · 0.43 · वर्ष: 1990; सम्मान: पद्म विभूषण; टिप्पणी: भारत का दूसरा सर्वोच्च नागरिक पुरस्कार।
  *5. p16 · #50 · 0.43 · वर्ष: 1997; सम्मान: भारत रत्न; टिप्पणी: भारत का सर्वोच्च नागरिक सम्मान।
   6. p16 · #48 · 0.41 · वर्ष: 1981; सम्मान: पद्म भूषण; टिप्पणी: विज्ञान एवं इंजीनियरिंग में योगदान के लिए।
   7. p16 · #51 · 0.34 · वर्ष: 1997; सम्मान: राष्ट्रीय एकता के लिए इंदिरा गांधी पुरस्कार
   8. p16 · #52 · 0.28 · वर्ष: विभिन्न; सम्मान: मानद डॉक्टरेट; टिप्पणी: विश्व भर के चालीस से अधिक विश्वविद्यालयों स
  judge: supported   · Kalam was awarded the Bharat Ratna in 1997.
```

### 9. (en)

```text
Query   : What role did Kalam play in Pokhran-II?
Answer  : Kalam played a central organizational role in Pokhran-II as the Scientific Adviser to the Defence Minister and the head of DRDO, working alongside scientists from the Department of Atomic Energy.
Source  : page: 10 · section: "पोखरण-II: 1998 के परमाणु परीक्षण" · chunk_id: 27 · score: 0.51
Latency : retrieval 424 ms + LLM first token 584 ms = end-to-end TTFT 1,008 ms (LLM complete after 670 ms)  [groq:qwen/qwen3.8-27b]
Retrieved context (rank · page · chunk_id · score):
  *1. p10 · #27 · 0.51 · मई 1998 में, भारत ने राजस्थान के पोखरण में भूमिगत परमाणु परीक्षणों की एक शृंखला की, जिसे प
   2. p19 · #69 · 0.45 · कलाम की विरासत कई दिशाओं में फैली है। विज्ञान में, उन्होंने भारत को उपग्रह प्रक्षेपण यानों
   3. p10 · #28 · 0.43 · ये परीक्षण कड़ी गोपनीयता और सटीक समन्वय के साथ किए गए, और इन्होंने भारत की सामरिक स्थिति म
   4. p3 · #3 · 0.42 · अवुल पाकिर जैनुलाब्दीन अब्दुल कलाम (1931–2015) एक भारतीय एयरोस्पेस वैज्ञानिक तथा भारत के ग
  judge: supported   · Kalam played a central organizational role in Pokhran-II.
  judge: supported   · Kalam was the Scientific Adviser to the Defence Minister during Pokhran-II.
  judge: supported   · Kalam was the head of DRDO during Pokhran-II.
  judge: supported   · Kalam worked alongside scientists from the Department of Atomic Energy during Pokhran-II.
```

### 10. (hi)

```text
Query   : कलाम ने वैमानिकी इंजीनियरिंग किस संस्थान से पढ़ी?
Answer  : कलाम ने वैमानिकी इंजीनियरिंग चेन्नई के मद्रास इंस्टीट्यूट ऑफ टेक्नोलॉजी (एमआईटी) से पढ़ी।
Source  : page: 6 · section: "कॉलेज के वर्ष और उड़ान का आकर्षण" · chunk_id: 12 · score: 0.70
          page: 20 · section: "संस्थाओं एवं शब्दों की शब्दावली" · chunk_id: 77 · score: 0.66
Latency : retrieval 388 ms + LLM first token 777 ms = end-to-end TTFT 1,165 ms (LLM complete after 986 ms)  [groq:qwen/qwen3.8-27b]
Retrieved context (rank · page · chunk_id · score):
  *1. p6 · #12 · 0.70 · उन्होंने वैमानिकी इंजीनियरिंग पढ़ने के लिए चेन्नई के मद्रास इंस्टीट्यूट ऑफ टेक्नोलॉजी (एमआ
   2. p6 · #11 · 0.69 · स्कूल के बाद, कलाम ने तिरुचिरापल्ली के सेंट जोसेफ कॉलेज में भौतिकी पढ़ी और 1950 के दशक के 
  *3. p20 · #77 · 0.66 · एमआईटी (चेन्नई): मद्रास इंस्टीट्यूट ऑफ टेक्नोलॉजी, जहाँ कलाम ने वैमानिकी पढ़ी।
   4. p7 · #14 · 0.59 · कलाम ने अपना व्यावसायिक जीवन भारत के रक्षा प्रतिष्ठान के अंग, तकनीकी विकास एवं उत्पादन निद
  judge: supported   · कलाम ने वैमानिकी इंजीनियरिंग चेन्नई के मद्रास इंस्टीट्यूट ऑफ टेक्नोलॉजी (एमआईटी) से पढ़ी।
```

### 11. (hi)

```text
Query   : अग्नि की उड़ान किसके साथ मिलकर लिखी गई और कब प्रकाशित हुई?
Answer  : अग्नि की उड़ान वैज्ञानिक अरुण तिवारी के साथ मिलकर लिखी गई थी और इसका प्रकाशन 1999 में हुआ था।
Source  : page: 3 · section: "ए.पी.जे. अब्दुल कलाम कौन थे?" · chunk_id: 4 · score: 0.60
          page: 17 · section: "जीवन-रेखा (टाइमलाइन)" · chunk_id: 63 · score: 0.58
          page: 22 · section: "त्वरित तथ्य-सारांश" · chunk_id: 91 · score: 0.57
Latency : retrieval 383 ms + LLM first token 1,373 ms = end-to-end TTFT 1,756 ms (LLM complete after 1,472 ms)  [groq:qwen/qwen3.8-27b]
Retrieved context (rank · page · chunk_id · score):
  *1. p3 · #4 · 0.60 · अग्नि की उड़ान, जो 1999 में प्रकाशित हुई और वैज्ञानिक अरुण तिवारी के साथ मिलकर लिखी गई, उन
  *2. p17 · #63 · 0.58 · 1999: अग्नि की उड़ान प्रकाशित (अरुण तिवारी के साथ)।
  *3. p22 · #91 · 0.57 · आत्मकथा: अग्नि की उड़ान (1999), अरुण तिवारी के साथ
   4. p1 · #0 · 0.52 · अग्नि की उड़ान ए.पी.जे. अब्दुल कलाम का जीवन, कार्य और विचार अवुल पाकिर जैनुलाब्दीन अब्दुल 
  judge: supported   · अग्नि की उड़ान वैज्ञानिक अरुण तिवारी के साथ मिलकर लिखी गई थी
  judge: supported   · अग्नि की उड़ान का प्रकाशन 1999 में हुआ था
```

### 12. (hi)

```text
Query   : कलाम का निधन कहाँ और कैसे हुआ?
Answer  : कलाम का निधन 27 जुलाई 2015 को शिलांग के भारतीय प्रबंधन संस्थान में विद्यार्थियों को व्याख्यान देते समय गिरने के कुछ ही देर बाद हुआ।
Source  : page: 15 · section: "अंतिम क्षण तक शिक्षक (2007–2015)" · chunk_id: 46 · score: 0.63
Latency : retrieval 355 ms + LLM first token 649 ms = end-to-end TTFT 1,004 ms (LLM complete after 773 ms)  [groq:qwen/qwen3.8-27b]
Retrieved context (rank · page · chunk_id · score):
  *1. p15 · #46 · 0.63 · 27 जुलाई 2015 को, कलाम शिलांग के भारतीय प्रबंधन संस्थान में विद्यार्थियों को व्याख्यान देत
   2. p3 · #3 · 0.59 · अवुल पाकिर जैनुलाब्दीन अब्दुल कलाम (1931–2015) एक भारतीय एयरोस्पेस वैज्ञानिक तथा भारत के ग
   3. p4 · #5 · 0.58 · कलाम का जन्म 15 अक्टूबर 1931 को तमिलनाडु के दक्षिण-पूर्वी तट के निकट पम्बन द्वीप पर स्थित 
   4. p6 · #12 · 0.52 · उन्होंने वैमानिकी इंजीनियरिंग पढ़ने के लिए चेन्नई के मद्रास इंस्टीट्यूट ऑफ टेक्नोलॉजी (एमआ
  judge: supported   · कलाम का निधन 27 जुलाई 2015 को हुआ।
  judge: supported   · कलाम का निधन शिलांग के भारतीय प्रबंधन संस्थान में विद्यार्थियों को व्याख्यान देते समय गिरने के कुछ ही देर बाद हुआ।
```

### 13. (en)

```text
Query   : What are the names of the missiles developed under the IGMDP and what do the names mean?
Answer  : The missiles developed under the IGMDP are Nag (meaning "Nag/Cobra"), Prithvi (meaning "Earth"), Agni (meaning "Fire"), Trishul (meaning "Trishul"), and Akash (meaning "Sky").
Source  : page: 9 · section: "निर्देशित मिसाइल कार्यक्रम" · chunk_id: 25 · score: 0.44
          page: 9 · section: "निर्देशित मिसाइल कार्यक्रम" · chunk_id: 21 · score: 0.42
          page: 9 · section: "निर्देशित मिसाइल कार्यक्रम" · chunk_id: 22 · score: 0.41
          page: 9 · section: "निर्देशित मिसाइल कार्यक्रम" · chunk_id: 23 · score: 0.41
          page: 9 · section: "निर्देशित मिसाइल कार्यक्रम" · chunk_id: 24 · score: 0.40
Latency : retrieval 475 ms + LLM first token 875 ms = end-to-end TTFT 1,350 ms (LLM complete after 990 ms)  [groq:qwen/qwen3.8-27b]
Retrieved context (rank · page · chunk_id · score):
   1. p9 · #20 · 0.65 · 1980 के दशक के आरंभ में कलाम रक्षा अनुसंधान एवं विकास संगठन (डीआरडीओ) में एकीकृत निर्देशित
   2. p20 · #74 · 0.62 · IGMDP: एकीकृत निर्देशित मिसाइल विकास कार्यक्रम, डीआरडीओ में कलाम के नेतृत्व में।
   3. p22 · #89 · 0.46 · प्रमुख कार्यक्रम (डीआरडीओ): एकीकृत निर्देशित मिसाइल विकास कार्यक्रम
  *4. p9 · #25 · 0.44 · मिसाइल: नाग; प्रकार (भूमिका): टैंक-रोधी निर्देशित मिसाइल; नाम का अर्थ: "नाग/कोबरा"
  *5. p9 · #21 · 0.42 · मिसाइल: पृथ्वी; प्रकार (भूमिका): सतह-से-सतह, कम दूरी; नाम का अर्थ: "धरती"
  *6. p9 · #22 · 0.41 · मिसाइल: अग्नि; प्रकार (भूमिका): सतह-से-सतह, अधिक दूरी; नाम का अर्थ: "आग"
  *7. p9 · #23 · 0.41 · मिसाइल: त्रिशूल; प्रकार (भूमिका): कम दूरी की सतह-से-हवा; नाम का अर्थ: "त्रिशूल"
  *8. p9 · #24 · 0.40 · मिसाइल: आकाश; प्रकार (भूमिका): मध्यम दूरी की सतह-से-हवा; नाम का अर्थ: "आसमान"
  judge: supported   · Nag is a missile developed under IGMDP.
  judge: supported   · The name Nag means "Nag/Cobra".
  judge: supported   · Prithvi is a missile developed under IGMDP.
  judge: supported   · The name Prithvi means "Earth".
  judge: supported   · Agni is a missile developed under IGMDP.
  judge: supported   · The name Agni means "Fire".
  judge: supported   · Trishul is a missile developed under IGMDP.
  judge: supported   · The name Trishul means "Trishul".
  judge: supported   · Akash is a missile developed under IGMDP.
  judge: supported   · The name Akash means "Sky".
```

### 14. (en)

```text
Query   : Why did Kalam not become a fighter pilot?
Answer  : Kalam did not become a fighter pilot because he narrowly missed selection for the Indian Air Force, finishing in ninth place when only eight positions were available.
Source  : page: 6 · section: "कॉलेज के वर्ष और उड़ान का आकर्षण" · chunk_id: 13 · score: 0.50
Latency : retrieval 368 ms + LLM first token 842 ms = end-to-end TTFT 1,210 ms (LLM complete after 906 ms)  [groq:qwen/qwen3.8-27b]
Retrieved context (rank · page · chunk_id · score):
  *1. p6 · #13 · 0.50 · लड़ाकू विमान चालक (फाइटर पायलट) बनने का उनका सपना पूरा नहीं हुआ। उन्होंने भारतीय वायुसेना 
   2. p3 · #3 · 0.48 · अवुल पाकिर जैनुलाब्दीन अब्दुल कलाम (1931–2015) एक भारतीय एयरोस्पेस वैज्ञानिक तथा भारत के ग
   3. p6 · #11 · 0.46 · स्कूल के बाद, कलाम ने तिरुचिरापल्ली के सेंट जोसेफ कॉलेज में भौतिकी पढ़ी और 1950 के दशक के 
   4. p3 · #4 · 0.45 · अग्नि की उड़ान, जो 1999 में प्रकाशित हुई और वैज्ञानिक अरुण तिवारी के साथ मिलकर लिखी गई, उन
  judge: supported   · Kalam did not become a fighter pilot.
  judge: supported   · He narrowly missed selection for the Indian Air Force.
  judge: supported   · He finished in ninth place when only eight positions were available.
```

### 15. (en)

```text
Query   : How did Satish Dhawan handle the 1979 launch failure?
Answer  : Satish Dhawan publicly took responsibility for the 1979 launch failure and protected his team.
Source  : page: 8 · section: "इसरो के वर्ष और SLV-III" · chunk_id: 18 · score: 0.58
          page: 12 · section: "गुरु एवं शिक्षक" · chunk_id: 38 · score: 0.46
Latency : retrieval 403 ms + LLM first token 1,748 ms = end-to-end TTFT 2,151 ms (LLM complete after 1,826 ms)  [groq:qwen/qwen3.8-27b]
Retrieved context (rank · page · chunk_id · score):
  *1. p8 · #18 · 0.58 · यह रास्ता सहज नहीं था। 1979 में एक आरंभिक प्रक्षेपण प्रयास विफल हो गया जब यान उड़ान भरने क
  *2. p12 · #38 · 0.46 · सतीश धवन: इसरो प्रमुख जिन्होंने विफलता आत्मसात की और श्रेय बाँटा — कलाम का नेतृत्व-आदर्श।
   3. p8 · #19 · 0.45 · जुलाई 1980 में, SLV-III ने रोहिणी उपग्रह को सफलतापूर्वक कक्षा में स्थापित किया, जिससे भारत
   4. p17 · #58 · 0.45 · 1979: पहला SLV-III प्रक्षेपण प्रयास विफल।
   5. p12 · #37 · 0.32 · विक्रम साराभाई: भारत के अंतरिक्ष प्रयास के जनक; कलाम को आरंभ में विश्वास और ज़िम्मेदारी दी
   6. p12 · #39 · 0.28 · ब्रह्म प्रकाश: वरिष्ठ वैज्ञानिक और प्रक्षेपण-यान वर्षों में स्थिर मार्गदर्शक।
   7. p12 · #36 · 0.21 · रेव. आयडुरई सोलोमन: स्कूल-गुरु जिन्होंने ऊँचा लक्ष्य रखना और सफलता की अपेक्षा करना सिखाया।
   8. p12 · #35 · 0.17 · जैनुलाब्दीन (पिता): कर्तव्य, आस्था, ईमानदारी और सादगी से जीना सिखाया।
  judge: supported   · Satish Dhawan publicly took responsibility for the 1979 launch failure.
  judge: supported   · Satish Dhawan protected his team.
```

### 16. (hi)

```text
Query   : कलाम को "जनता के राष्ट्रपति" क्यों कहा गया?
Answer  : कलाम को उनकी गर्मजोशी, सुलभता और आम नागरिकों, विशेषकर विद्यार्थियों के साथ अथक संवाद के कारण "जनता के राष्ट्रपति" कहा गया।
Source  : page: 14 · section: "जनता के राष्ट्रपति (2002–2007)" · chunk_id: 43 · score: 0.71
Latency : retrieval 396 ms + LLM first token 547 ms = end-to-end TTFT 942 ms (LLM complete after 662 ms)  [groq:qwen/qwen3.8-27b]
Retrieved context (rank · page · chunk_id · score):
  *1. p14 · #43 · 0.71 · 2002 में, कलाम भारत के ग्यारहवें राष्ट्रपति चुने गए, उसी वर्ष जुलाई में पद ग्रहण किया और 2
   2. p14 · #44 · 0.68 · कलाम इस पद पर एक वैज्ञानिक की आदतें लेकर आए: जिज्ञासा, सीधी बात, और बहानों के प्रति अधीरता
   3. p3 · #3 · 0.64 · अवुल पाकिर जैनुलाब्दीन अब्दुल कलाम (1931–2015) एक भारतीय एयरोस्पेस वैज्ञानिक तथा भारत के ग
   4. p15 · #45 · 0.58 · 2007 में राष्ट्रपति पद छोड़ने के बाद, कलाम उस काम की ओर लौटे जो उन्हें सबसे प्रिय था: शिक्
  judge: supported   · कलाम को उनकी गर्मजोशी के कारण "जनता के राष्ट्रपति" कहा गया।
  judge: supported   · कलाम को उनकी सुलभता के कारण "जनता के राष्ट्रपति" कहा गया।
  judge: supported   · कलाम को आम नागरिकों के साथ अथक संवाद के कारण "जनता के राष्ट्रपति" कहा गया।
  judge: supported   · कलाम को विशेषकर विद्यार्थियों के साथ अथक संवाद के कारण "जनता के राष्ट्रपति" कहा गया।
```

### 17. (en)

```text
Query   : Who was Vikram Sarabhai?
Answer  : Vikram Sarabhai was a visionary physicist widely regarded as the father of India's space program.
Source  : page: 7 · section: "वैज्ञानिक करियर के पहले कदम" · chunk_id: 15 · score: 0.48
          page: 12 · section: "गुरु एवं शिक्षक" · chunk_id: 37 · score: 0.42
Latency : retrieval 376 ms + LLM first token 691 ms = end-to-end TTFT 1,067 ms (LLM complete after 721 ms)  [groq:qwen/qwen3.8-27b]
Retrieved context (rank · page · chunk_id · score):
  *1. p7 · #15 · 0.48 · निर्णायक मोड़ तब आया जब वे भारतीय अंतरिक्ष अनुसंधान समिति में शामिल हुए, जो इसरो की पूर्वव
  *2. p12 · #37 · 0.42 · विक्रम साराभाई: भारत के अंतरिक्ष प्रयास के जनक; कलाम को आरंभ में विश्वास और ज़िम्मेदारी दी
   3. p3 · #3 · 0.39 · अवुल पाकिर जैनुलाब्दीन अब्दुल कलाम (1931–2015) एक भारतीय एयरोस्पेस वैज्ञानिक तथा भारत के ग
   4. p8 · #19 · 0.38 · जुलाई 1980 में, SLV-III ने रोहिणी उपग्रह को सफलतापूर्वक कक्षा में स्थापित किया, जिससे भारत
   5. p12 · #38 · 0.29 · सतीश धवन: इसरो प्रमुख जिन्होंने विफलता आत्मसात की और श्रेय बाँटा — कलाम का नेतृत्व-आदर्श।
   6. p12 · #35 · 0.27 · जैनुलाब्दीन (पिता): कर्तव्य, आस्था, ईमानदारी और सादगी से जीना सिखाया।
   7. p12 · #39 · 0.25 · ब्रह्म प्रकाश: वरिष्ठ वैज्ञानिक और प्रक्षेपण-यान वर्षों में स्थिर मार्गदर्शक।
   8. p12 · #36 · 0.22 · रेव. आयडुरई सोलोमन: स्कूल-गुरु जिन्होंने ऊँचा लक्ष्य रखना और सफलता की अपेक्षा करना सिखाया।
  judge: supported   · Vikram Sarabhai was a visionary physicist.
  judge: supported   · Vikram Sarabhai is widely regarded as the father of India's space program.
```

### 18. (en)

```text
Query   : When and where was Kalam born?
Answer  : Kalam was born on October 15, 1931, in Rameswaram, Tamil Nadu.
Source  : page: 4 · section: "रामेश्वरम में बचपन" · chunk_id: 5 · score: 0.54
          page: 17 · section: "जीवन-रेखा (टाइमलाइन)" · chunk_id: 54 · score: 0.43
Latency : retrieval 286 ms + LLM first token 1,060 ms = end-to-end TTFT 1,346 ms (LLM complete after 1,128 ms)  [groq:qwen/qwen3.8-27b]
Retrieved context (rank · page · chunk_id · score):
  *1. p4 · #5 · 0.54 · कलाम का जन्म 15 अक्टूबर 1931 को तमिलनाडु के दक्षिण-पूर्वी तट के निकट पम्बन द्वीप पर स्थित 
   2. p3 · #3 · 0.48 · अवुल पाकिर जैनुलाब्दीन अब्दुल कलाम (1931–2015) एक भारतीय एयरोस्पेस वैज्ञानिक तथा भारत के ग
  *3. p17 · #54 · 0.43 · 1931: 15 अक्टूबर को तमिलनाडु के रामेश्वरम में जन्म।
   4. p6 · #12 · 0.41 · उन्होंने वैमानिकी इंजीनियरिंग पढ़ने के लिए चेन्नई के मद्रास इंस्टीट्यूट ऑफ टेक्नोलॉजी (एमआ
  judge: supported   · Kalam was born on October 15, 1931.
  judge: supported   · Kalam was born in Rameswaram, Tamil Nadu.
```

### 19. (hi)

```text
Query   : कलाम ने बचपन में अख़बार क्यों बाँटे?
Answer  : द्वितीय विश्वयुद्ध के दौरान रेल सेवाओं में बाधा के कारण कलाम ने चलती ट्रेन से गिराए गए अख़बार एकत्रित करके बाँटे, जिससे उन्हें अपना पहला स्वयं कमाया धन मिला।
Source  : page: 4 · section: "रामेश्वरम में बचपन" · chunk_id: 7 · score: 0.58
Latency : retrieval 467 ms + LLM first token 723 ms = end-to-end TTFT 1,190 ms (LLM complete after 871 ms)  [groq:qwen/qwen3.8-27b]
Retrieved context (rank · page · chunk_id · score):
   1. p4 · #5 · 0.60 · कलाम का जन्म 15 अक्टूबर 1931 को तमिलनाडु के दक्षिण-पूर्वी तट के निकट पम्बन द्वीप पर स्थित 
   2. p4 · #6 · 0.59 · 1930 के दशक का रामेश्वरम ऐसा स्थान था जहाँ विभिन्न समुदाय मिल-जुलकर रहते थे। कलाम एक मुस्ल
   3. p5 · #9 · 0.58 · कलाम ने घर से थोड़ी दूर रामनाथपुरम के श्वार्ट्ज़ हायर सेकेंडरी स्कूल में शिक्षा पाई। वे एक
  *4. p4 · #7 · 0.58 · बालक के रूप में उन्होंने परिवार की आय बढ़ाने के लिए छोटे-मोटे काम किए। द्वितीय विश्वयुद्ध 
  judge: supported   · द्वितीय विश्वयुद्ध के दौरान रेल सेवाओं में बाधा के कारण कलाम ने चलती ट्रेन से गिराए गए अख़बार एकत्रित करके बाँटे।
  judge: supported   · इससे उन्हें अपना पहला स्वयं कमाया धन मिला।
```

### 20. (en)

```text
Query   : Who helped Kalam pay his college fees?
Answer  : His sister helped pay his college fees by pawning her jewelry.
Source  : page: 6 · section: "कॉलेज के वर्ष और उड़ान का आकर्षण" · chunk_id: 12 · score: 0.51
Latency : retrieval 410 ms + LLM first token 760 ms = end-to-end TTFT 1,170 ms (LLM complete after 795 ms)  [groq:qwen/qwen3.8-27b]
Retrieved context (rank · page · chunk_id · score):
  *1. p6 · #12 · 0.51 · उन्होंने वैमानिकी इंजीनियरिंग पढ़ने के लिए चेन्नई के मद्रास इंस्टीट्यूट ऑफ टेक्नोलॉजी (एमआ
   2. p6 · #11 · 0.42 · स्कूल के बाद, कलाम ने तिरुचिरापल्ली के सेंट जोसेफ कॉलेज में भौतिकी पढ़ी और 1950 के दशक के 
   3. p5 · #10 · 0.41 · घर पर, उनके पिता एक भिन्न किंतु समान रूप से स्थायी शिक्षा देते थे — कर्तव्य, प्रार्थना और 
   4. p4 · #5 · 0.40 · कलाम का जन्म 15 अक्टूबर 1931 को तमिलनाडु के दक्षिण-पूर्वी तट के निकट पम्बन द्वीप पर स्थित 
  judge: supported   · His sister helped pay his college fees.
  judge: supported   · She pawned her jewelry to do so.
```

### 21. (en)

```text
Query   : What is the population of Tokyo?
Answer  : The document does not contain an answer to this question.
Source  : — (no supporting passage found)
Latency : retrieval 314 ms + LLM first token 705 ms = end-to-end TTFT 1,019 ms (LLM complete after 711 ms)  [groq:qwen/qwen3.8-27b]
Retrieved context (rank · page · chunk_id · score):
   1. p17 · #54 · 0.37 · 1931: 15 अक्टूबर को तमिलनाडु के रामेश्वरम में जन्म।
   2. p3 · #3 · 0.36 · अवुल पाकिर जैनुलाब्दीन अब्दुल कलाम (1931–2015) एक भारतीय एयरोस्पेस वैज्ञानिक तथा भारत के ग
   3. p22 · #83 · 0.32 · जन्म: 15 अक्टूबर 1931, रामेश्वरम, तमिलनाडु
   4. p4 · #5 · 0.31 · कलाम का जन्म 15 अक्टूबर 1931 को तमिलनाडु के दक्षिण-पूर्वी तट के निकट पम्बन द्वीप पर स्थित 
```

### 22. (en)

```text
Query   : Who won the 2018 FIFA World Cup?
Answer  : The document does not contain an answer to this question.
Source  : — (no supporting passage found)
Latency : retrieval 363 ms + LLM first token 592 ms = end-to-end TTFT 955 ms (LLM complete after 596 ms)  [groq:qwen/qwen3.8-27b]
Retrieved context (rank · page · chunk_id · score):
   1. p3 · #3 · 0.43 · अवुल पाकिर जैनुलाब्दीन अब्दुल कलाम (1931–2015) एक भारतीय एयरोस्पेस वैज्ञानिक तथा भारत के ग
   2. p19 · #69 · 0.37 · कलाम की विरासत कई दिशाओं में फैली है। विज्ञान में, उन्होंने भारत को उपग्रह प्रक्षेपण यानों
   3. p3 · #4 · 0.36 · अग्नि की उड़ान, जो 1999 में प्रकाशित हुई और वैज्ञानिक अरुण तिवारी के साथ मिलकर लिखी गई, उन
   4. p22 · #82 · 0.36 · पूरा नाम: अवुल पाकिर जैनुलाब्दीन अब्दुल कलाम
```

### 23. (hi)

```text
Query   : पाइथन प्रोग्रामिंग भाषा किसने बनाई?
Answer  : दस्तावेज़ में इस प्रश्न का उत्तर उपलब्ध नहीं है।
Source  : — (no supporting passage found)
Latency : retrieval 368 ms + LLM first token 1,448 ms = end-to-end TTFT 1,816 ms (LLM complete after 1,455 ms)  [groq:qwen/qwen3.8-27b]
Retrieved context (rank · page · chunk_id · score):
   1. p9 · #20 · 0.39 · 1980 के दशक के आरंभ में कलाम रक्षा अनुसंधान एवं विकास संगठन (डीआरडीओ) में एकीकृत निर्देशित
   2. p9 · #26 · 0.38 · कलाम का दृष्टिकोण तकनीकी गहराई को बड़ी, विविध टीमों को वर्षों के कठिन काम के दौरान एकजुट र
   3. p3 · #4 · 0.37 · अग्नि की उड़ान, जो 1999 में प्रकाशित हुई और वैज्ञानिक अरुण तिवारी के साथ मिलकर लिखी गई, उन
   4. p3 · #3 · 0.37 · अवुल पाकिर जैनुलाब्दीन अब्दुल कलाम (1931–2015) एक भारतीय एयरोस्पेस वैज्ञानिक तथा भारत के ग
```
