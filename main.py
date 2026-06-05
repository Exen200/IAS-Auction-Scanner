import os, json, threading, webbrowser, requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk, messagebox

DB_FILE='seen_links.json'
OUT_DIR='WYNIKI'
HEADERS={'User-Agent':'Mozilla/5.0'}
SOURCES={
 'Katowice':'https://www.gov.pl/web/ias-katowice/obwieszczenia-o-licytacjach',
 'Wroclaw':'https://www.gov.pl/web/ias-wroclaw/obwieszczenia-o-licytacjach',
 'Poznan':'https://www.wielkopolskie.kas.gov.pl/izba-administracji-skarbowej-w-poznaniu/ogloszenia/obwieszczenia-o-licytacjach',
 'Opole':'https://www.opolskie.kas.gov.pl/izba-administracji-skarbowej-w-opolu/ogloszenia/obwieszczenia-o-licytacjach'
}
BAD=['nieruchomo','dzialka','lokal','mieszkan','grunt','udzial']
GOOD=['samoch','pojazd','ruchomo','motocy','maszyn','sprzet','komputer','bmw','audi','opel']

def load_seen():
    if os.path.exists(DB_FILE):
        return set(json.load(open(DB_FILE,'r',encoding='utf-8')))
    return set()

def save_seen(s):
    json.dump(sorted(list(s)), open(DB_FILE,'w',encoding='utf-8'), ensure_ascii=False, indent=2)

def is_ruchomosc(title):
    t=title.lower()
    if any(x in t for x in BAD): return False
    return any(x in t for x in GOOD) or 'licytacj' in t

def fetch(url):
    r=requests.get(url,headers=HEADERS,timeout=20)
    r.raise_for_status(); return r.text

def parse_links(base):
    from urllib.parse import urljoin
    visited=[]; out=[]
    for p in range(1,16):
        url = base if p==1 else (base + (('&' if '?' in base else '?') + f'page={p}&size=20'))
        try:
            html=fetch(url)
        except:
            continue
        soup=BeautifulSoup(html,'html.parser')
        page_count=0
        for a in soup.select('a[href]'):
            href=a.get('href','')
            txt=' '.join(a.stripped_strings).strip()
            if not txt:
                continue
            if href.startswith('/'):
                href=urljoin(base,href)
            if href.startswith('http') and ('licyt' in txt.lower() or 'obwieszc' in href.lower()):
                key=(txt,href)
                if key not in visited:
                    visited.append(key)
                    out.append(key)
                    page_count+=1
        if page_count==0 and p>3:
            break
    return out

class App:
    def __init__(self,root):
        self.root=root; root.title('MONITOR LICYTACJI KAS'); root.geometry('700x500'); root.configure(bg='#1e1e1e')
        tk.Label(root,text='MONITOR LICYTACJI KAS',fg='white',bg='#1e1e1e',font=('Segoe UI',16,'bold')).pack(pady=10)
        self.status=tk.Label(root,text='Status: Gotowy',fg='white',bg='#1e1e1e'); self.status.pack()
        self.pb=ttk.Progressbar(root,length=500,mode='determinate'); self.pb.pack(pady=8)
        fr=tk.Frame(root,bg='#1e1e1e'); fr.pack(pady=5)
        tk.Button(fr,text='SPRAWDŹ TERAZ',command=self.start,bg='#2e7d32',fg='white').grid(row=0,column=0,padx=5)
        tk.Button(fr,text='OTWÓRZ WYNIKI',command=self.open_results,bg='#444',fg='white').grid(row=0,column=1,padx=5)
        tk.Button(fr,text='ZAMKNIJ',command=root.destroy,bg='#666',fg='white').grid(row=0,column=2,padx=5)
        self.log=tk.Text(root,height=20,bg='#111',fg='#ddd'); self.log.pack(fill='both',expand=True,padx=10,pady=10)
    def write(self,msg): self.log.insert('end',msg+'\n'); self.log.see('end'); self.root.update()
    def open_results(self):
        if os.path.exists(OUT_DIR): os.startfile(OUT_DIR)
    def start(self): threading.Thread(target=self.run,daemon=True).start()
    def run(self):
        seen=load_seen(); new=[]; self.pb['value']=0; total=len(SOURCES)
        for i,(name,url) in enumerate(SOURCES.items(),1):
            self.status.config(text=f'Sprawdzam {name}...')
            self.write(f'{name}: start')
            try:
                for title,link in parse_links(url):
                    if link not in seen and is_ruchomosc(title):
                        new.append((name,title,link)); seen.add(link)
                count=len(parse_links(url)); self.write(f'{name}: OK ({count} wpisów)')
            except Exception as e:
                self.write(f'{name}: BŁĄD {e}')
            self.pb['value']=i/total*100; self.root.update()
        save_seen(seen)
        if new:
            os.makedirs(OUT_DIR,exist_ok=True)
            from datetime import date
            outfile=os.path.join(OUT_DIR,f'{date.today().isoformat()}.txt')
            with open(outfile,'w',encoding='utf-8') as f:
                for n,t,l in new:
                                        f.write(f'[{n}]\n{t}\n{l}\n\n')
            self.status.config(text=f'Znaleziono {len(new)} nowych ogłoszeń')
            messagebox.showinfo('Gotowe',f'Znaleziono {len(new)} nowych ogłoszeń')
        else:
            self.status.config(text='Brak nowych ruchomości')
            messagebox.showinfo('Gotowe','Brak nowych ruchomości')

if __name__=='__main__':
    root=tk.Tk(); App(root); root.mainloop()
