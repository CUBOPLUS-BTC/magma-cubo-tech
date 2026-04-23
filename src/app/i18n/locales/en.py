"""
English (en) translations for Magma Bitcoin app.
All API responses, error messages, achievement descriptions, and notification templates.
"""

TRANSLATIONS: dict = {

    # -----------------------------------------------------------------------
    # Auth
    # -----------------------------------------------------------------------
    "auth.challenge.issued":        "Challenge issued successfully.",
    "auth.challenge.expired":       "Challenge has expired. Please request a new one.",
    "auth.challenge.not_found":     "No challenge found for this public key.",
    "auth.challenge.mismatch":      "Challenge mismatch. Authentication failed.",
    "auth.challenge.required":      "A challenge string is required.",
    "auth.pubkey.required":         "A public key (pubkey) is required.",
    "auth.pubkey.invalid":          "Invalid public key format. Expected 64 hex characters.",
    "auth.success":                 "Authentication successful.",
    "auth.failure":                 "Authentication failed. Please check your credentials.",
    "auth.session.created":         "Session created. You are now logged in.",
    "auth.session.invalid":         "Session token is invalid or has expired.",
    "auth.session.expired":         "Your session has expired. Please log in again.",
    "auth.session.revoked":         "Session revoked successfully.",
    "auth.session.not_found":       "Session not found.",
    "auth.rate_limited":            "Too many authentication attempts. Please wait {wait_seconds} seconds.",
    "auth.nostr.event.required":    "A signed Nostr event is required.",
    "auth.nostr.event.invalid":     "The signed Nostr event is invalid.",
    "auth.nostr.pubkey.mismatch":   "The event pubkey does not match the requested public key.",
    "auth.lnurl.challenge.invalid": "LNURL authentication challenge is invalid.",
    "auth.lnurl.signature.invalid": "LNURL signature verification failed.",
    "auth.permission.denied":       "You do not have permission to perform this action.",
    "auth.phone.invalid":           "Invalid phone number. Use Salvadoran format (+503 XXXX-XXXX).",
    "auth.phone.code.sent":         "Code sent via SMS.",
    "auth.phone.code.invalid":      "Wrong code. Please try again.",
    "auth.phone.code.expired":      "Code has expired. Request a new one.",

    # -----------------------------------------------------------------------
    # Savings
    # -----------------------------------------------------------------------
    "savings.goal.set":             "Savings goal updated successfully.",
    "savings.goal.not_found":       "No savings goal configured. Set one to get started.",
    "savings.goal.required":        "A savings goal is required for this action.",
    "savings.deposit.recorded":     "Deposit of {amount} recorded successfully.",
    "savings.deposit.invalid_amount": "Deposit amount must be a positive number.",
    "savings.deposit.not_found":    "Deposit record not found.",
    "savings.projection.generated": "Savings projection generated.",
    "savings.projection.no_data":   "Not enough data to generate a projection. Make at least one deposit.",
    "savings.monthly_target":       "Monthly savings target",
    "savings.total_saved":          "Total saved",
    "savings.total_btc":            "Total BTC accumulated",
    "savings.target_years":         "Target years",
    "savings.on_track":             "You are on track to reach your goal!",
    "savings.behind_target":        "You are currently behind your monthly target.",
    "savings.ahead_target":         "You are ahead of your monthly savings target.",
    "savings.no_deposits":          "No deposits recorded yet. Start saving today!",

    # -----------------------------------------------------------------------
    # Remittance
    # -----------------------------------------------------------------------
    "remittance.calculation.success": "Remittance calculation completed.",
    "remittance.amount.invalid":    "Please enter a valid remittance amount.",
    "remittance.currency.invalid":  "Invalid currency code. Please use a 3-letter ISO code.",
    "remittance.rate.unavailable":  "Exchange rate is temporarily unavailable. Try again shortly.",
    "remittance.fee.breakdown":     "Fee breakdown",
    "remittance.recipient.receives": "Recipient receives",
    "remittance.sender.pays":       "Sender pays",
    "remittance.via_bitcoin":       "Via Bitcoin (instant)",
    "remittance.via_traditional":   "Via traditional wire (3-5 business days)",
    "remittance.savings_vs_traditional": "Savings vs. traditional remittance",
    "remittance.no_data":           "Remittance data is not available at this time.",

    # -----------------------------------------------------------------------
    # Pension
    # -----------------------------------------------------------------------
    "pension.projection.generated": "Pension projection generated.",
    "pension.projection.no_data":   "Please configure your savings goal to generate a pension projection.",
    "pension.age.required":         "Current age is required for pension calculation.",
    "pension.age.invalid":          "Age must be between 18 and 80.",
    "pension.retirement_age":       "Target retirement age",
    "pension.years_to_retire":      "Years until retirement",
    "pension.projected_value":      "Projected portfolio value at retirement",
    "pension.monthly_income":       "Estimated monthly income",
    "pension.inflation_adjusted":   "Inflation-adjusted value",
    "pension.on_track":             "You are on track for a comfortable retirement.",
    "pension.underfunded":          "Your current savings rate may not meet your retirement goal.",
    "pension.increase_savings":     "Consider increasing your monthly savings to meet your goal.",

    # -----------------------------------------------------------------------
    # Market
    # -----------------------------------------------------------------------
    "market.price.unavailable":     "Bitcoin price data is temporarily unavailable.",
    "market.price.fetched":         "Market price retrieved successfully.",
    "market.fees.unavailable":      "On-chain fee data is temporarily unavailable.",
    "market.fees.fetched":          "Fee estimates retrieved successfully.",
    "market.history.unavailable":   "Price history is temporarily unavailable.",
    "market.history.fetched":       "Price history retrieved successfully.",
    "market.loading":               "Loading market data…",
    "market.last_updated":          "Last updated",

    # -----------------------------------------------------------------------
    # Alerts
    # -----------------------------------------------------------------------
    "alerts.preferences.updated":  "Alert preferences updated.",
    "alerts.preferences.not_found": "No alert preferences found. Using defaults.",
    "alerts.fee.triggered":         "Bitcoin fee alert: {direction} {level} sat/vB",
    "alerts.price.triggered":       "Bitcoin price alert: {direction} {price}",
    "alerts.fee.high":              "Fees are HIGH — currently {fee} sat/vB.",
    "alerts.fee.low":               "Fees are LOW — currently {fee} sat/vB. Good time to transact!",
    "alerts.price.above":           "BTC price crossed above {threshold}.",
    "alerts.price.below":           "BTC price dropped below {threshold}.",
    "alerts.enabled":               "Alerts are enabled.",
    "alerts.disabled":              "Alerts are disabled.",

    # -----------------------------------------------------------------------
    # Achievements
    # -----------------------------------------------------------------------
    "achievements.earned":          "Achievement unlocked: {name}!",
    "achievements.none":            "No achievements yet. Start saving to earn your first badge!",
    "achievements.all_fetched":     "Achievements loaded.",

    # Achievement names
    "achievement.first_deposit.name":       "First Steps",
    "achievement.first_deposit.desc":       "Made your first Bitcoin savings deposit.",
    "achievement.hodl_week.name":           "Week HODLer",
    "achievement.hodl_week.desc":           "Saved consistently for an entire week.",
    "achievement.hodl_month.name":          "Monthly Stacker",
    "achievement.hodl_month.desc":          "Maintained your savings habit for 30 days.",
    "achievement.goal_setter.name":         "Goal Setter",
    "achievement.goal_setter.desc":         "Set your first savings goal.",
    "achievement.diamond_hands.name":       "Diamond Hands",
    "achievement.diamond_hands.desc":       "Held your Bitcoin through a 10% market dip.",
    "achievement.satoshi_100k.name":        "100K Sats",
    "achievement.satoshi_100k.desc":        "Accumulated 100,000 satoshis.",
    "achievement.satoshi_1m.name":          "1M Sats",
    "achievement.satoshi_1m.desc":          "Accumulated 1,000,000 satoshis.",
    "achievement.satoshi_10m.name":         "10M Sats",
    "achievement.satoshi_10m.desc":         "Accumulated 10,000,000 satoshis.",
    "achievement.on_track.name":            "On Track",
    "achievement.on_track.desc":            "Stayed on track with your savings plan for a full month.",
    "achievement.nostr_auth.name":          "Nostr Native",
    "achievement.nostr_auth.desc":          "Authenticated using Nostr (NIP-07).",
    "achievement.streak_7.name":            "7-Day Streak",
    "achievement.streak_7.desc":            "Deposited every day for 7 consecutive days.",
    "achievement.streak_30.name":           "30-Day Streak",
    "achievement.streak_30.desc":           "Deposited every day for 30 consecutive days.",
    "achievement.early_adopter.name":       "Early Adopter",
    "achievement.early_adopter.desc":       "One of the first 100 users on Magma.",
    "achievement.big_saver.name":           "Big Saver",
    "achievement.big_saver.desc":           "Saved over $500 in a single month.",
    "achievement.lightning_fast.name":      "Lightning Fast",
    "achievement.lightning_fast.desc":      "Completed a Lightning Network payment.",

    # -----------------------------------------------------------------------
    # Notifications
    # -----------------------------------------------------------------------
    "notification.welcome.title":       "Welcome to Magma!",
    "notification.welcome.body":        "Start your Bitcoin savings journey today. Set a goal and make your first deposit.",
    "notification.deposit.title":       "Deposit Confirmed",
    "notification.deposit.body":        "Your deposit of {amount} has been recorded. You've saved {total} so far.",
    "notification.achievement.title":   "Achievement Unlocked!",
    "notification.achievement.body":    'You earned the "{name}" badge. Keep stacking!',
    "notification.goal_reached.title":  "Savings Goal Reached!",
    "notification.goal_reached.body":   "Congratulations! You have reached your savings goal of {goal}.",
    "notification.price_alert.title":   "Bitcoin Price Alert",
    "notification.price_alert.body":    "BTC is now {direction} {threshold}. Current price: {price}.",
    "notification.fee_alert.title":     "Fee Alert",
    "notification.fee_alert.body":      "On-chain fees are now {level}: {fee} sat/vB.",
    "notification.streak.title":        "Savings Streak!",
    "notification.streak.body":         "You are on a {days}-day savings streak. Don't break it!",
    "notification.monthly_summary.title": "Monthly Summary",
    "notification.monthly_summary.body":  "This month you saved {amount}. Your total is now {total}.",

    # -----------------------------------------------------------------------
    # Export
    # -----------------------------------------------------------------------
    "export.generated":             "Export generated successfully.",
    "export.format.pdf":            "PDF Export",
    "export.format.csv":            "CSV Export",
    "export.format.json":           "JSON Export",
    "export.no_data":               "No data available to export.",
    "export.savings_report":        "Savings Report",
    "export.remittance_report":     "Remittance Report",
    "export.pension_report":        "Pension Projection Report",
    "export.generated_by":          "Generated by Magma",
    "export.generated_on":          "Generated on",
    "export.confidential":          "Confidential — for personal use only.",

    # -----------------------------------------------------------------------
    # Compliance / Admin
    # -----------------------------------------------------------------------
    "compliance.aml.low":           "Low risk transaction.",
    "compliance.aml.medium":        "Medium risk — monitoring required.",
    "compliance.aml.high":          "High risk — manual review required.",
    "compliance.aml.critical":      "Critical risk — transaction blocked pending review.",
    "compliance.ctr.required":      "Currency Transaction Report required for ${amount}.",
    "compliance.sar.drafted":       "Suspicious Activity Report drafted.",
    "compliance.alert.pending":     "Compliance alert pending review.",
    "compliance.alert.resolved":    "Compliance alert resolved.",
    "compliance.sanctioned_address": "This address is on a sanctions list. Transaction blocked.",
    "compliance.jurisdiction.sv":   "El Salvador (UAF)",
    "compliance.jurisdiction.us":   "United States (FinCEN)",
    "compliance.jurisdiction.eu":   "European Union (EBA)",

    "admin.access.denied":          "Admin access denied.",
    "admin.access.not_configured":  "Admin access is not configured on this server.",
    "admin.action.completed":       "Admin action completed successfully.",
    "admin.user.banned":            "User {pubkey} has been banned.",
    "admin.user.unbanned":          "User {pubkey} ban has been lifted.",
    "admin.maintenance.completed":  "Maintenance completed in {elapsed_ms}ms.",
    "admin.config.updated":         "Configuration key '{key}' updated.",
    "admin.config.blocked":         "Configuration key '{key}' cannot be modified at runtime.",

    # -----------------------------------------------------------------------
    # Errors
    # -----------------------------------------------------------------------
    "error.not_found":              "The requested resource was not found.",
    "error.bad_request":            "The request is malformed or missing required fields.",
    "error.unauthorized":           "Authentication is required.",
    "error.forbidden":              "You do not have permission to access this resource.",
    "error.rate_limited":           "Too many requests. Please slow down.",
    "error.internal":               "An internal server error occurred. Please try again.",
    "error.database":               "A database error occurred. Please contact support.",
    "error.validation.string":      "Field '{field}' must be a string.",
    "error.validation.number":      "Field '{field}' must be a number.",
    "error.validation.range":       "Field '{field}' must be between {min} and {max}.",
    "error.validation.required":    "Field '{field}' is required.",
    "error.validation.invalid":     "Field '{field}' has an invalid value.",
    "error.injection.detected":     "Potentially malicious input detected in field '{field}'.",
    "error.sanitization.failed":    "Input could not be sanitized for field '{field}'.",
    "error.method.not_allowed":     "HTTP method not allowed for this endpoint.",
    "error.payload.too_large":      "Request payload exceeds the maximum allowed size.",
    "error.timeout":                "The request timed out. Please try again.",
    "error.service.unavailable":    "This service is temporarily unavailable.",
    "error.bitcoin.address":        "Invalid Bitcoin address.",
    "error.lightning.invoice":      "Invalid Lightning Network invoice.",
    "error.nostr.pubkey":           "Invalid Nostr public key.",
    "error.amount.negative":        "Amount cannot be negative.",
    "error.amount.zero":            "Amount cannot be zero.",
    "error.amount.too_large":       "Amount exceeds the maximum allowed value.",
    "error.date.invalid":           "Invalid date format. Expected YYYY-MM-DD.",
    "error.currency.invalid":       "Invalid currency code.",
    "error.json.invalid":           "Invalid JSON payload.",

    # -----------------------------------------------------------------------
    # Portfolio
    # -----------------------------------------------------------------------
    "portfolio.summary":            "Portfolio Summary",
    "portfolio.current_value":      "Current portfolio value",
    "portfolio.total_invested":     "Total amount invested",
    "portfolio.unrealized_gain":    "Unrealized gain/loss",
    "portfolio.return_pct":         "Total return",
    "portfolio.btc_price_avg":      "Average buy price",
    "portfolio.holdings":           "Holdings",
    "portfolio.no_data":            "No portfolio data available. Make your first deposit to get started.",

    # -----------------------------------------------------------------------
    # General UI
    # -----------------------------------------------------------------------
    "general.loading":              "Loading…",
    "general.saving":               "Saving…",
    "general.success":              "Success!",
    "general.error":                "An error occurred.",
    "general.cancel":               "Cancel",
    "general.confirm":              "Confirm",
    "general.save":                 "Save",
    "general.delete":               "Delete",
    "general.edit":                 "Edit",
    "general.view":                 "View",
    "general.back":                 "Back",
    "general.next":                 "Next",
    "general.previous":             "Previous",
    "general.close":                "Close",
    "general.search":               "Search",
    "general.filter":               "Filter",
    "general.sort":                 "Sort",
    "general.export":               "Export",
    "general.import":               "Import",
    "general.refresh":              "Refresh",
    "general.yes":                  "Yes",
    "general.no":                   "No",
    "general.none":                 "None",
    "general.all":                  "All",
    "general.today":                "Today",
    "general.yesterday":            "Yesterday",
    "general.this_week":            "This week",
    "general.this_month":           "This month",
    "general.days_ago":             "{n} days ago",
    "general.hours_ago":            "{n} hours ago",
    "general.minutes_ago":          "{n} minutes ago",
    "general.just_now":             "Just now",
    "general.unknown":              "Unknown",
    "general.n_a":                  "N/A",

    # -----------------------------------------------------------------------
    # Scoring
    # -----------------------------------------------------------------------
    "scoring.address.required":     "address is required",
    "scoring.address.invalid":      "Invalid Bitcoin address format: {address}",
    "scoring.analysis.failed":      "Analysis failed: {error}",
    "scoring.address_query.required": "address query parameter is required",

    # -----------------------------------------------------------------------
    # Preferences
    # -----------------------------------------------------------------------
    "preferences.auth.required":    "Authentication required",
    "preferences.load.failed":      "Could not load preferences: {error}",
    "preferences.body.empty":       "Request body must not be empty",
    "preferences.fields.invalid":   "No valid fields provided. Accepted: fee_alert_low, fee_alert_high, alerts_enabled",
    "preferences.update.failed":    "Could not update preferences: {error}",
    "preferences.price_usd.required": "price_usd is required",
    "preferences.price_usd.invalid": "price_usd must be a number",
    "preferences.direction.required": "direction is required",
    "preferences.alert.created":    "Price alert created",
    "preferences.alert.add_failed": "Could not add alert: {error}",
    "preferences.alert_id.required": "alert_id is required",
    "preferences.alert.removed":    "Price alert removed",
    "preferences.alert.remove_failed": "Could not remove alert: {error}",

    # -----------------------------------------------------------------------
    # Lightning
    # -----------------------------------------------------------------------
    "lightning.overview.failed":    "Could not fetch Lightning overview: {error}",
    "lightning.compare.failed":     "Could not generate comparison: {error}",
    "lightning.amount.required":    "amount_usd is required (body or query parameter)",
    "lightning.amount.invalid":     "amount_usd must be a number",
    "lightning.amount.positive":    "amount_usd must be positive",
    "lightning.urgency.invalid":    "urgency must be one of: low, medium, high, instant",
    "lightning.recommend.failed":   "Recommendation failed: {error}",

    # -----------------------------------------------------------------------
    # Webhooks
    # -----------------------------------------------------------------------
    "webhooks.auth.required":       "Authentication required",
    "webhooks.url.required":        "url is required",
    "webhooks.events.required":     "events must be a non-empty list",
    "webhooks.events.unsupported":  "Unsupported event type(s): {events}",
    "webhooks.subscribe.failed":    "Failed to create subscription: {error}",
    "webhooks.subscribe.success":   "Subscription created. Store the secret — it will not be shown again.",
    "webhooks.sub_id.required":     "subscription_id is required",
    "webhooks.unsubscribe.failed":  "Failed to remove subscription: {error}",
    "webhooks.unsubscribe.not_found": "Subscription not found",
    "webhooks.unsubscribe.success": "Subscription deleted",
    "webhooks.list.failed":         "Failed to list subscriptions: {error}",
    "webhooks.update.fields":       "No valid fields to update (url, events, active)",
    "webhooks.update.not_found":    "Subscription not found",
    "webhooks.update.failed":       "Update failed: {error}",
    "webhooks.test.success":        "Test webhook delivered successfully.",
    "webhooks.test.failed":         "Test webhook delivery failed.",
    "webhooks.test.hint":           "Check that the URL is reachable and returns a 2xx status.",

    # -----------------------------------------------------------------------
    # Market
    # -----------------------------------------------------------------------
    "market.days.range":            "days must be between 1 and 365",
    "market.interval.invalid":      "interval must be 'daily' or 'hourly'",
    "market.prices.minimum":        "Need at least 20 price points",
    "market.signal_type.required":  "signal_type required for backtest mode",
    "market.mode.invalid":          "mode must be 'summary', 'score', or 'backtest'",
    "market.no_price_data":         "No price data available",

    # -----------------------------------------------------------------------
    # Portfolio
    # -----------------------------------------------------------------------
    "portfolio.amount.positive":    "amount must be positive",
    "portfolio.price.positive":     "price_usd must be positive",
    "portfolio.tx_type.invalid":    "invalid tx_type",
    "portfolio.period.invalid":     "period must be 'day', 'week', 'month', 'year', or 'all'",
    "portfolio.assets.required":    "assets list required",
    "portfolio.assets.mismatch":    "assets and expected_returns must have same length",
    "portfolio.method.invalid":     "method must be 'basic', 'min_variance', 'max_sharpe', or 'risk_parity'",
    "portfolio.no_holdings":        "No holdings found",
    "portfolio.risk_note":          "Stress test results show estimated portfolio impact under each predefined market scenario.",
    "portfolio.cost_method.invalid": "method must be 'fifo', 'lifo', or 'average'",
    "portfolio.target.required":    "target_allocation required",

    # -----------------------------------------------------------------------
    # Simulation
    # -----------------------------------------------------------------------
    "simulation.initial.nonneg":    "initial must be non-negative",
    "simulation.monthly.nonneg":    "monthly_contribution must be non-negative",
    "simulation.years.range":       "years must be between 1 and 50",
    "simulation.amount.positive":   "amount must be positive",
    "simulation.frequency.invalid": "frequency must be 'daily', 'weekly', or 'monthly'",
    "simulation.years.range_30":    "years must be between 1 and 30",
    "simulation.prices.required":   "prices list is required",
    "simulation.prices.minimum":    "Need at least 20 price data points",
    "simulation.strategy.unknown":  "Unknown strategy: {name}",
    "simulation.scenario.required": "scenario name or custom_scenario required for single mode",
    "simulation.mode.invalid":      "mode must be 'single', 'stress_test', or 'list'",
    "simulation.price.positive":    "current_price must be positive",
    "simulation.volatility.range":  "volatility must be between 0 and 5",
    "simulation.days.range":        "days must be between 1 and 3650",
    "simulation.age.invalid":       "current_age must be less than retirement_age",
    "simulation.retire.invalid":    "retirement_age must be less than life_expectancy",
    "simulation.portfolio.positive": "portfolio_value must be positive",
    "simulation.withdrawals.positive": "monthly_withdrawals must be positive",

    # -----------------------------------------------------------------------
    # Stats
    # -----------------------------------------------------------------------
    "stats.data.required":          "Missing required field: data",
    "stats.data.list":              "Field 'data' must be a list of numbers.",
    "stats.data.empty":             "Field 'data' must not be empty.",
    "stats.data.too_large":         "data exceeds maximum of {max} points.",
    "stats.data.non_numeric":       "data contains non-numeric values: {error}",
    "stats.include.list":           "Field 'include' must be a list of strings.",
    "stats.x.required":             "Missing required field: x",
    "stats.y.required":             "Missing required field: y",
    "stats.xy.list":                "Fields 'x' and 'y' must be lists.",
    "stats.xy.length":              "x (len={x_len}) and y (len={y_len}) must have equal length.",
    "stats.xy.minimum_2":           "At least 2 data points are required for correlation.",
    "stats.xy.minimum_3":           "At least 3 data points are required for regression.",
    "stats.xy.too_large":           "Data exceeds {max} points.",
    "stats.xy.non_numeric":         "Non-numeric values: {error}",
    "stats.methods.list":           "Field 'methods' must be a list.",
    "stats.regression.type_invalid": "Invalid type. Use 'linear', 'log_linear', or 'power_law'.",
    "stats.regression.failed":      "Regression failed: {error}",

    # -----------------------------------------------------------------------
    # Liquid
    # -----------------------------------------------------------------------
    "liquid.overview.failed":       "Could not fetch Liquid overview: {error}",
    "liquid.assets.failed":         "Could not fetch Liquid assets: {error}",
    "liquid.compare.failed":        "Could not generate comparison: {error}",
    "liquid.peg.failed":            "Could not fetch peg info: {error}",
    "liquid.amount.required":       "amount_usd is required",
    "liquid.amount.invalid":        "amount_usd must be a number",
    "liquid.amount.positive":       "amount_usd must be positive",
    "liquid.urgency.invalid":       "urgency must be one of: low, medium, high, instant",
    "liquid.privacy.invalid":       "privacy must be one of: normal, high, confidential",
    "liquid.recommend.failed":      "Recommendation failed: {error}",

    # -----------------------------------------------------------------------
    # Recipients
    # -----------------------------------------------------------------------
    "recipients.auth.required":     "Authentication required",
    "recipients.body.invalid":      "Invalid body",
    "recipients.created":           "Recipient created",
    "recipients.create.failed":     "Error creating recipient: {error}",
    "recipients.list.failed":       "Could not list recipients: {error}",
    "recipients.get.failed":        "Error fetching recipient: {error}",
    "recipients.body.empty":        "Empty body",
    "recipients.updated":           "Recipient updated",
    "recipients.update.failed":     "Error updating: {error}",
    "recipients.not_found":         "Recipient not found",
    "recipients.deleted":           "Recipient deleted",
    "recipients.delete.failed":     "Error deleting: {error}",

    # -----------------------------------------------------------------------
    # Reminders
    # -----------------------------------------------------------------------
    "reminders.auth.required":      "Authentication required",
    "reminders.body.invalid":       "Invalid body",
    "reminders.recipient_id.required": "recipient_id required (integer)",
    "reminders.created":            "Reminder created",
    "reminders.create.failed":      "Error creating reminder: {error}",
    "reminders.list.failed":        "Error listing reminders: {error}",
    "reminders.body.empty":         "Empty body",
    "reminders.updated":            "Reminder updated",
    "reminders.not_found":          "Reminder not found",
    "reminders.deleted":            "Reminder deleted",

    # -----------------------------------------------------------------------
    # Sends
    # -----------------------------------------------------------------------
    "sends.auth.required":          "Authentication required",
    "sends.body.invalid":           "Invalid body",
    "sends.recipient_id.required":  "recipient_id required (integer)",
    "sends.amount.required":        "amount_usd required (numeric)",
    "sends.invoice.failed":         "Error generating invoice: {error}",

    # -----------------------------------------------------------------------
    # Splits (non-custodial remittance router)
    # -----------------------------------------------------------------------
    "splits.label.required":        "label is required",
    "splits.profile.not_found":     "Split profile not found",
    "splits.rules.required":        "A list of rules is required",
    "splits.profile_id.required":   "profile_id required (integer)",
    "splits.amount.required":       "amount_usd required (numeric)",
    "splits.build.failed":          "Error building split: {error}",

    # -----------------------------------------------------------------------
    # Admin (extra)
    # -----------------------------------------------------------------------
    "admin.target.required":        "target_pubkey is required",
    "admin.user.not_found":         "User not found",
    "admin.token.required":         "token is required for action=revoke",
    "admin.action.unknown":         "Unknown action: {action}",
    "admin.key.required":           "key is required for action=set",
    "admin.delete.confirm":         "Set confirm='DELETE' to confirm irreversible deletion",

    # -----------------------------------------------------------------------
    # Export (extra)
    # -----------------------------------------------------------------------
    "export.pubkey.invalid":        "Invalid pubkey",
    "export.dates.integer":         "date_from and date_to must be integers",
    "export.year_month.integer":    "year and month must be integers",
    "export.month.range":           "month must be between 1 and 12",
    "export.year.range":            "year out of valid range",
    "export.amount.number":         "amount_usd must be a number",
    "export.amount.positive":       "amount_usd must be positive",
    "export.numeric.invalid":       "Invalid numeric parameter",
    "export.monthly.positive":      "monthly_usd must be positive",
    "export.years.range":           "years must be between 1 and 50",
    "export.report_type.unknown":   "Unknown report_type '{type}'. Valid values: savings, statement, remittance, pension",

    # -----------------------------------------------------------------------
    # Locale validation
    # -----------------------------------------------------------------------
    "locale.invalid":               "Invalid locale. Use 'en' or 'es'.",
}
