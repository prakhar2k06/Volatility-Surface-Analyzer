def prepare_surface_grid(df, contract_type="call"):
    temp = df.copy()

    temp = temp[temp["contract_type"] == contract_type]

    temp = temp[temp["final_iv"].notna()]
    temp = temp[temp["final_iv"] > 0]

    quality_rank: dict[str, int] = {
        "high": 3,
        "medium": 2,
        "low": 1,
    }

    iv_source_rank: dict[str, int] = {
        "computed": 3,
        "provider_fallback": 2,
        "provider": 1,
        "unavailable": 0,
    }

    temp["quality_rank"] = temp["quality_flag"].map(quality_rank).fillna(0)
    temp["iv_source_rank"] = temp["iv_source"].map(iv_source_rank).fillna(0)

    temp = temp.sort_values(
        by=[
            "strike",
            "time_to_expiry",
            "quality_rank",
            "iv_source_rank",
            "openInterest",
            "volume",
        ],
        ascending=[True, True, False, False, False, False],
    )

    temp = temp.drop_duplicates(
        subset=["strike", "time_to_expiry"],
        keep="first",
    )

    surface = temp.pivot(
        index="strike",
        columns="time_to_expiry",
        values="final_iv",
    )
    surface = surface.sort_index()
    surface = surface.reindex(sorted(surface.columns), axis=1)

    return surface
