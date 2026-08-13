import tkinter as tk
from tkinter import messagebox, simpledialog
import random
from ctypes import windll

# High DPI setting for Windows (윈도우 고해상도 DPI 설정)
try:
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

class StockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Wide Monitor Edition (와이드 모니터 에디션)")
        self.root.geometry("1280x850") 
        self.root.state('zoomed') 
        self.root.configure(bg="#f8f9fa")

        # Asset Data (자산 데이터)
        self.money = 1000000 
        self.day = 1
        self.stocks = {
            "Python Electronics (파이썬전자)": {"price": 50000, "yesterday_price": 50000, "count": 0, "avg_price": 0, "history": [50000]},
            "C Lang Entertainment (C언어엔터)": {"price": 30000, "yesterday_price": 30000, "count": 0, "avg_price": 0, "history": [30000]},
            "JS Confectionery (JS제과)": {"price": 15000, "yesterday_price": 15000, "count": 0, "avg_price": 0, "history": [15000]},
            "Linux Software (리눅스소프트)": {"price": 80000, "yesterday_price": 80000, "count": 0, "avg_price": 0, "history": [80000]}
        }
        
        self.game_timer = 60
        self.is_market_open = True
        self.current_selected = "Python Electronics (파이썬전자)"

        # --- Top Header (상단 헤더) ---
        self.header = tk.Frame(root, bg="#2c3e50", pady=15)
        self.header.pack(fill="x")
        self.label_day = tk.Label(self.header, text=f"📅 Day {self.day} (제 {self.day}일차)", font=("Malgun Gothic", 12), fg="#1abc9c", bg="#2c3e50")
        self.label_day.pack()
        self.label_money = tk.Label(self.header, text=f"💰 Balance (잔고): {self.money:,} KRW (원)", font=("Malgun Gothic", 20, "bold"), fg="white", bg="#2c3e50")
        self.label_money.pack(pady=5)
        self.label_timer = tk.Label(self.header, text=f"⏱️ Time Left (마감까지): {self.game_timer}s (초)", font=("Malgun Gothic", 11), fg="#f1c40f", bg="#2c3e50")
        self.label_timer.pack()

        # News Feed (뉴스 피드)
        self.news_frame = tk.Frame(root, bg="#fff9c4", bd=1, relief="flat")
        self.news_frame.pack(fill="x", padx=30, pady=15)
        self.label_news = tk.Label(self.news_frame, text="📢 Watch today's market situation! (오늘의 시장 상황을 주시하세요!)", font=("Malgun Gothic", 11, "bold"), bg="#fff9c4", height=2)
        self.label_news.pack()

        # --- [Center] Chart Area ([중앙] 차트 영역) ---
        self.center_area = tk.Frame(root, bg="#ffffff", bd=1, relief="solid")
        self.center_area.pack(fill="x", padx=30, pady=10)
        self.graph_title = tk.Label(self.center_area, text=f"📊 [{self.current_selected}] Real-time Chart (실시간 차트)", font=("Malgun Gothic", 12, "bold"), bg="white", pady=10)
        self.graph_title.pack()
        self.canvas = tk.Canvas(self.center_area, width=750, height=200, bg="#ffffff", highlightthickness=0)
        self.canvas.pack(pady=5)
        
        self.info_board = tk.Frame(self.center_area, bg="#f1f3f5", pady=12)
        self.info_board.pack(fill="x")
        self.label_yest_info = tk.Label(self.info_board, text="Calculating data... (데이터 계산 중...)", font=("Malgun Gothic", 11, "bold"), bg="#f1f3f5")
        self.label_yest_info.pack()

        # --- [Bottom] Stock List ([하단] 종목 리스트) ---
        self.list_frame = tk.Frame(root, bg="#f8f9fa")
        self.list_frame.pack(fill="both", expand=True, padx=30, pady=10)

        self.stock_uis = {}
        for name in self.stocks.keys():
            card = tk.Frame(self.list_frame, bg="white", pady=10, padx=15)
            card.pack(fill="x", pady=4)
            
            # 1. Stock name (neatly aligned with a width of 32) (1. 종목 이름 (너비 32로 깔끔하게 정돈))
            btn_name = tk.Button(card, text=name, font=("Malgun Gothic", 11, "bold"), bg="#ecf0f1", width=32, anchor="w", command=lambda n=name: self.select_stock(n))
            btn_name.pack(side="left", padx=(5, 10))

            # 2. Current price display (2. 현재가 표시)
            price_label = tk.Label(card, text="0 KRW (0.0%)", font=("Consolas", 11, "bold"), bg="white", width=22, anchor="w")
            price_label.pack(side="left", padx=5)

            # 3. Buy / Sell buttons (3. 매수 / 매도 버튼)
            btn_frame = tk.Frame(card, bg="white")
            btn_frame.pack(side="left", padx=5)
            tk.Button(btn_frame, text="Buy (매수)", bg="#e74c3c", fg="white", width=8, font=("Malgun Gothic", 9, "bold"), command=lambda n=name: self.buy_stock(n)).pack(side="left", padx=2)
            tk.Button(btn_frame, text="Sell (매도)", bg="#3498db", fg="white", width=8, font=("Malgun Gothic", 9, "bold"), command=lambda n=name: self.sell_stock(n)).pack(side="left", padx=2)

            # 4. Holdings and average purchase price info (aligned to the right + positioned immediately next to it using side="left"!) (4. 보유 및 평단가 정보 (오른쪽 붙이기 + side="left"로 바로 옆에 이어지게!))
            profit_label = tk.Label(card, text="Not Owned (보유 없음)", font=("Malgun Gothic", 10), bg="white", fg="#95a5a6", anchor="e")
            profit_label.pack(side="right", fill="x", expand=True, padx=(10, 5))
            
            self.stock_uis[name] = {"price": price_label, "btn": btn_name, "profit": profit_label}

        self.update_loop()
        self.news_loop()

    def select_stock(self, name):
        self.current_selected = name
        self.graph_title.config(text=f"📊 [{self.current_selected}] Real-time Chart (실시간 차트)")
        self.draw_graph()
        self.update_info_board()

    def update_info_board(self):
        d = self.stocks[self.current_selected]
        diff = d["price"] - d["yesterday_price"]
        rate = (diff / d["yesterday_price"]) * 100 if d["yesterday_price"] != 0 else 0
        color = "#e74c3c" if diff > 0 else ("#3498db" if diff < 0 else "black")
        self.label_yest_info.config(text=f"Prev. Close (전일 종가): {d['yesterday_price']:,} KRW (원)  |  Current Change (현재 변동): {diff:+,} KRW (원) ({rate:+.1f}%)", fg=color)

    def update_loop(self):
        if self.is_market_open:
            self.game_timer -= 1
            self.label_timer.config(text=f"⏱️ Time Left (마감까지): {self.game_timer}s (초)")
            
            for name, data in self.stocks.items():
                # 1. Price Fluctuation (가격 변동)
                change = random.uniform(-0.015, 0.015) 
                new_p = int(data["price"] * (1 + change))
                
                # 2. Upper/Lower Price Limit (상/하한가 제한)
                limit_up = int(data["yesterday_price"] * 1.30)
                limit_down = int(data["yesterday_price"] * 0.70)
                new_p = max(500, min(new_p, limit_up, max(new_p, limit_down)))
                
                data["price"] = new_p
                data["history"].append(new_p)

                # 3. UI Update - Price List (UI 업데이트 - 리스트 가격)
                m_rate = ((data["price"] - data["yesterday_price"]) / data["yesterday_price"]) * 100
                m_color = "#e74c3c" if m_rate > 0 else ("#3498db" if m_rate < 0 else "black")
                status_text = f"{data['price']:,} KRW ({m_rate:+.1f}%)"
                if data["price"] == limit_up: status_text += " [Upper (상)]"
                if data["price"] == limit_down: status_text += " [Lower (하)]"
                self.stock_uis[name]["price"].config(text=status_text, fg=m_color)

                # 4. Update Holdings Info (보유 정보 업데이트)
                if data["count"] > 0:
                    profit = (data["price"] - data["avg_price"]) * data["count"]
                    p_rate = (profit / (data["avg_price"] * data["count"])) * 100
                    p_color = "#e74c3c" if profit > 0 else ("#3498db" if profit < 0 else "#95a5a6")
                    self.stock_uis[name]["profit"].config(
                        text=f"Owned (보유): {data['count']} shares (주) | Avg (평단): {data['avg_price']:,} KRW (원) | {profit:+,} KRW (원) ({p_rate:+.1f}%)", fg=p_color
                    )
                else:
                    self.stock_uis[name]["profit"].config(text="Not Owned (보유 없음)", fg="#95a5a6")

            self.update_info_board()
            self.draw_graph()
            
            if self.game_timer <= 0:
                self.close_market()
            else:
                self.root.after(1000, self.update_loop)

    def draw_graph(self):
        self.canvas.delete("all")
        h_list = self.stocks[self.current_selected]["history"][-50:]
        if len(h_list) < 2: return
        mx, mn = max(h_list)*1.02, min(h_list)*0.98
        if mx == mn: mx += 10
        w, h = 750, 200
        step = w / (len(h_list) - 1)
        for i in range(len(h_list)-1):
            x1, y1 = i*step, h - ((h_list[i]-mn)/(mx-mn)*h)
            x2, y2 = (i+1)*step, h - ((h_list[i+1]-mn)/(mx-mn)*h)
            color = "#e74c3c" if h_list[i+1] >= h_list[i] else "#3498db"
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2)

    def buy_stock(self, name):
        if not self.is_market_open: return
        p = self.stocks[name]["price"]
        ans = simpledialog.askstring("Buy (매수)", f"[{name}] Buy Quantity (구매 수량) (Balance/잔고: {self.money:,} KRW):")
        if ans:
            try:
                max_buy = self.money // p
                cnt = max_buy if ans.lower() == 'all' else int(ans)
                if 0 < cnt <= max_buy:
                    old_cost = self.stocks[name]["avg_price"] * self.stocks[name]["count"]
                    new_cost = p * cnt
                    self.stocks[name]["count"] += cnt
                    self.stocks[name]["avg_price"] = (old_cost + new_cost) // self.stocks[name]["count"]
                    self.money -= new_cost
                    self.label_money.config(text=f"💰 Balance (잔고): {self.money:,} KRW (원)")
                else:
                    messagebox.showwarning("Warning (경고)", "Insufficient balance or invalid quantity. (잔액이 부족하거나 잘못된 수량입니다.)")
            except: pass

    def sell_stock(self, name):
        if not self.is_market_open: return
        cnt_have = self.stocks[name]["count"]
        if cnt_have <= 0: return
        ans = simpledialog.askstring("Sell (매도)", f"[{name}] Sell Quantity (판매 수량) (Owned/보유: {cnt_have} shares/주):")
        if ans:
            try:
                cnt = cnt_have if ans.lower() == 'all' else int(ans)
                if 0 < cnt <= cnt_have:
                    self.money += self.stocks[name]["price"] * cnt
                    self.stocks[name]["count"] -= cnt
                    if self.stocks[name]["count"] == 0: self.stocks[name]["avg_price"] = 0
                    self.label_money.config(text=f"💰 Balance (잔고): {self.money:,} KRW (원)")
            except: pass

    def news_loop(self):
        if self.is_market_open:
            target = random.choice(list(self.stocks.keys()))
            news_db = [
                {"msg": f"{target}, record quarterly performance reported... 'Earnings Surprise' ({target}, 역대 최대 분기 실적 발표... '어닝 서프라이즈')", "effect": 0.12},
                {"msg": f"Foreign investors heavily buying {target}... 'Focus on Growth' (외국인 투자가, {target} 집중 매수세... '성장성 주목')", "effect": 0.05},
                {"msg": f"{target} signed exclusive supply deal for next-gen AI chips ({target}, 차세대 AI 칩 독점 공급 계약 체결)", "effect": 0.08},
                {"msg": f"Analysts say \"{target} is at the bottom... Raising target price\" (증권가 \"{target}, 지금이 바닥... 목표주가 상향 조정\")", "effect": 0.07},
                {"msg": f"{target} production line temporarily halted due to supply chain issues ({target}, 공급망 차질로 생산 라인 가동 일시 중단)", "effect": -0.08},
                {"msg": f"Fair Trade Commission investigates {target} for unfair trade allegations (공정위, {target} 대상 불공정 거래 혐의 조사 착수)", "effect": -0.12},
                {"msg": f"[Emergency] {target} Q3 operating profit halved... 'Earnings Shock' ([비상] {target}, 3분기 영업이익 반토막... '어닝 쇼크')", "effect": -0.15},
                {"msg": f"{target} defect reports received for new product... Full recall decided ({target}, 신제품 결함 신고 접수... 전량 리콜 결정)", "effect": -0.10}
            ]
            event = random.choice(news_db)
            self.stocks[target]["price"] = max(500, int(self.stocks[target]["price"] * (1 + event["effect"])))
            self.label_news.config(text=f"📰 {event['msg']}", fg="#000000" if event["effect"] > 0 else "#000000")
        
        self.root.after(10000, self.news_loop)

    def close_market(self):
        self.is_market_open = False
        # Dividend Logic (배당금 로직 - 전일 대비 상승 시 배당금 지급)
        div = sum(int((d["price"]-d["yesterday_price"])*0.05*d["count"]) for d in self.stocks.values() if d["count"]>0 and d["price"]>d["yesterday_price"])
        self.money += div
        for d in self.stocks.values(): d["yesterday_price"] = d["price"]
        self.label_money.config(text=f"💰 Balance (잔고): {self.money:,} KRW (원)")
        self.label_news.config(text=f"🌙 Market Closed! Dividends of {div:,} KRW deposited. (장 마감! 배당금 {div:,}원이 입금되었습니다.)", fg="#2c3e50")
        self.root.after(1000, lambda: self.rest_timer(10))


    def rest_timer(self, sec):
        if sec > 0:
            self.label_timer.config(text=f"🌙 Opening in {sec}s ({sec}초 후 개장)", fg="#e74c3c")
            self.root.after(1000, lambda: self.rest_timer(sec-1))
        else:
            self.day += 1
            self.is_market_open = True
            self.game_timer = 60
            self.label_day.config(text=f"📅 Day {self.day} (제 {self.day}일차)")
            self.label_timer.config(fg="#f1c40f")
            self.update_loop()

if __name__ == "__main__":
    root = tk.Tk()
    app = StockApp(root)
    root.mainloop()
