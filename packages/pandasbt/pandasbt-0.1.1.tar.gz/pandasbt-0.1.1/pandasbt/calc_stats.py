from pandas import DataFrame


def calc_stats(dataframe, price_column="close"):
    final_pnl = opt_df.final_pnl.iloc[-1]
    cum_profit = opt_df.cum_profit.iloc[-1]
    cum_cost = opt_df.cum_cost.iloc[-1]
    total_trades = opt_df[opt_df.signal!=0].shape[0]
    winners = opt_df[(opt_df.profit>0)].shape[0]
    win_ratio = 0
    if total_trades>0:
        trades_df = opt_df[opt_df.signal.shift(1)!=0]
        win_ratio = winners / total_trades
        profit_by_trade = final_pnl / total_trades
        sharpe_ratio = np.mean(trades_df.profit) / np.std(trades_df.profit) *np.sqrt(252)    
        sortino = np.mean(trades_df.profit) / np.std(trades_df.profit)*np.sqrt(252)
        loss_means = trades_df[trades_df.profit<0].profit.mean()
        win_means = trades_df[trades_df.profit>0].profit.mean()

    results[final_pnl] = {
        "p_entry": entry,
        "p_period": period,
        "final_pnl": final_pnl,
        "cum_profit": cum_profit,
        "total_trade": total_trades,
        "win_ratio": win_ratio,
        "profit_by_trade": profit_by_trade,
        "sharpe_ratio": sharpe_ratio,
        "sortino_ratio": sortino,
        "loss_means": loss_means,
        "win_means": win_means
    }
    return dataframe
