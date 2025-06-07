if position == "DEF" and player:
    opponent_row = schedule_df[
        (schedule_df["team"] == team_to_abbr.get(player, "")) &
        (schedule_df["week"] == current_week)
    ]
    opponent_abbr = opponent_row["opponent"].values[0] if not opponent_row.empty else ""

    offense_row = offense_df[offense_df["team"] == abbr_to_team.get(opponent_abbr, "")]
    
    total_rank = offense_row["total_offense_rank"].values[0] if not offense_row.empty else "??"
    rush_rank = offense_row["rush_rank"].values[0] if not offense_row.empty else "??"
    pass_rank = offense_row["pass_rank"].values[0] if not offense_row.empty else "??"

    # Emoji indicator based on offensive strength
    if total_rank <= 10:
        indicator = "⛔"
    elif 11 <= total_rank <= 20:
        indicator = "🟡"
    else:
        indicator = "✅"

    # Emoji for rushing offense rank
    if rush_rank <= 10:
        rush_indicator = "⛔"
    elif 11 <= rush_rank <= 20:
        rush_indicator = "🟡"
    else:
        rush_indicator = "✅"

    # Emoji for passing offense rank
    if pass_rank <= 10:
        pass_indicator = "⛔"
    elif 11 <= pass_rank <= 20:
        pass_indicator = "🟡"
    else:
        pass_indicator = "✅"

# ==== NEW stat column block (outside of col2) ====
    stat_col1, stat_col2 = st.columns(2)

    with stat_col1:
        st.markdown(f'<div style="margin-bottom: -8px;">{indicator} Opponent: {opponent_abbr} - {ordinal(total_rank)} Overall</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="margin-bottom: -8px;">{rush_indicator} Rushing Offense Rank: {ordinal(rush_rank)}</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="margin-bottom: -8px;">{pass_indicator} Passing Offense Rank: {ordinal(pass_rank)}</div>', unsafe_allow_html=True)

    with stat_col2:
        st.markdown(f'<div style="margin-bottom: -8px;">🔄 Turnovers Per Game: 1.4</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="margin-bottom: -8px;">💥 Sacks Allowed Per Game: 6.1</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="margin-bottom: -8px;">🧮 Implied Point Total: 13</div>', unsafe_allow_html=True)
