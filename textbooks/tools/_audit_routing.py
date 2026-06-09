import json, re
M = json.load(open("MANIFEST.json", encoding="utf-8"))
EV = json.load(open("ROUTING_EVAL.json", encoding="utf-8"))
STOP=set("with that this into from your you should what does mean give make build using like want need have them and the for are can how why when which who your our its was just then than also more most some any all into onto over under via per each both these those an to of in on is it do i me my we us be as at or if so no not new use used uses".split())
SHORT_OK=set("ui vr ar xr 2d 3d ai ml ip rl gi io os db ui ux api sql".split())
def norm(s): return re.sub(r"[^a-z0-9]+"," ",s.lower())
corpus={}
for b in M["books"]:
    corpus[b["id"]] = norm(" ".join([b["title"]," ".join(b["topics"])," ".join(b["key_concepts"]),b["summary"]]))
for d in M["reference_docs"]:
    corpus[d["id"]] = norm(" ".join([d["id"]," ".join(d.get("topics",[]))," ".join([d.get("summary","")])]))
def add(key, targets):
    for t in targets:
        tid = t if t.startswith("book_") else t.lower()
        if tid in corpus: corpus[tid] += " " + norm(key.replace("_"," "))
for k,v in M.get("topic_to_books",{}).items(): add(k,v)
for k,v in M.get("rag_hints",{}).items(): add(k,[t for t in v if isinstance(t,str) and not t.startswith("skills/")])
cwords={t:set(c.split()) for t,c in corpus.items()}
def match(t,ws):
    for w in ws:
        if t==w: return True
        if len(t)>=4 and t in w: return True
        if len(w)>=4 and w in t: return True
        if len(t)>=5 and len(w)>=5 and t[:4]==w[:4]: return True
    return False
def sig(q):
    toks=[t for t in norm(q).split() if (len(t)>=4 or t in SHORT_OK) and t not in STOP]
    return toks, [toks[i]+" "+toks[i+1] for i in range(len(toks)-1)]
def score(q,tid):
    toks,bg=sig(q); ws=cwords[tid]; c=corpus[tid]
    return sum(1 for t in toks if match(t,ws)) + sum(2 for b in bg if b in c)
passed=0; fails=[]
for case in EV["cases"]:
    q=case["query"]; expect=[e if e.startswith("book_") else e.lower() for e in case["expect"]]
    ranked=sorted(corpus, key=lambda t: score(q,t), reverse=True)
    top=[t for t in ranked if score(q,t)>0][:3]
    if any(e in top for e in expect): passed+=1
    else: fails.append((q,expect,[(t,score(q,t)) for t in ranked[:3]]))
print(f"Routing eval: {passed}/{len(EV['cases'])} passed")
for q,e,t in fails: print(f"\nQ: {q}\n  expected {e}\n  got {t}")
