# OCA moduli koje koristi bring.out

Većina ovih modula je pull-ovana sa https://github.com/OCA i koristi se bez izmjena.

Samo neki od njih su mijenjani:
1. payroll
2. report_xlsx
3. report_csv


## Korišteni moduli:
1. payroll
2. report_xlsx
3. report_csv
4. report_xml
5. account_asset_management
6. account_reconcile_oca
7. account_statement_base
8. account_statement_import_file
9. account_statement_import_file_reconcile_oca
10. auth_oidc
11. auth_oidc_environment
12. stock_mts_mto_rule
13. web_responsive
14. subscription_oca

## Napomene

report_xlsx i report_csv su "patchirani" da bi se omogućilo imenovanje CSV fajlova i podrška nestandardnom formatu CSV-a koji je potreban za modul [l10n_ba_pdv](https://github.com/bringout/l10n-bosnia/tree/main/l10n_ba_pdv). Kasnije sam primjetio da prave problem drugim reporting modulima.



