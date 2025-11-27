import matplotlib.pyplot as plt

def plotSignal(src, sig, fig_name: str="signals.png"):
        plt.figure(figsize=(12, 6))
        plt.plot(src.index, src["Close"], label="Close", color="deepskyblue", zorder=1)

        # buy signal
        buy_df = sig[sig["signal"] == 1]
        plt.scatter(
            buy_df["ts"], buy_df["close"],
            marker="^", s=60, label="Buy", color="red", zorder=2
        )

        # sell signal
        sell_df = sig[sig["signal"] == -1]
        plt.scatter(
            sell_df["ts"], sell_df["close"],
            marker="v", s=60, label="Sell", color="green", zorder=2
        )

        plt.title("Backtest Signals")
        plt.legend()
        plt.tight_layout()
        plt.savefig(fig_name, dpi=200)
        plt.close()
        print(f"Saved Signals Figure to {fig_name}")

def plotTrend(src, trend, fig_name: str="trends.png"):
        plt.figure(figsize=(12, 6))
        plt.plot(src.index, src["Close"], label="Close", color="deepskyblue")
        plt.plot(src.index, trend["up"], label="Upper Trend", linewidth=2, color="red")
        plt.plot(src.index, trend["dn"], label="Lower Trend", linewidth=2, color="green")
        
        plt.title("Backtest Trends")
        plt.legend()
        plt.tight_layout()
        plt.savefig(fig_name, dpi=200)
        plt.close()
        print(f"Saved Trends Figure to {fig_name}")