# CYBERSHIELD AI — CONTINUOUS AUDIT REPORT

Generated: 2026-09-06 16:39:32 UTC
Round: 1
Scope: Phase 1 -> Phase 15

## VERDICT: NOT PROVEN

## PHASE 1 — Authentication & Core Security

- [PASS] `backend/app/api`
- [PASS] `backend/app/core`
- [PASS] `backend/app/models`
- [PASS] `backend/app/schemas`
- [PASS] `backend/app/services`
- [PASS] `frontend/src/pages/Login.tsx`
- [PASS] `frontend/src/services`

Relevant implementation references:
- `frontend/src/App.tsx:9 -> login`
- `frontend/src/App.tsx:12 -> security`
- `frontend/src/App.tsx:17 -> security`
- `frontend/src/App.tsx:28 -> login`
- `frontend/src/App.tsx:29 -> login`
- `frontend/src/App.tsx:47 -> security`
- `frontend/src/App.tsx:48 -> security`
- `frontend/tests/routes.spec.ts:4 -> login`
- `frontend/tests/routes.spec.ts:8 -> security`
- `frontend/src/layouts/Sidebar.tsx:42 -> security`
- `frontend/src/layouts/Sidebar.tsx:44 -> security`
- `frontend/src/layouts/Sidebar.tsx:95 -> security`
- `frontend/src/layouts/Sidebar.tsx:111 -> security`
- `frontend/src/layouts/Topbar.tsx:28 -> security`
- `frontend/src/layouts/Topbar.tsx:39 -> security`
- `frontend/src/layouts/Topbar.tsx:66 -> security`
- `frontend/src/pages/AIChat.tsx:15 -> security`
- `frontend/src/pages/AIChat.tsx:16 -> security`
- `frontend/src/pages/AIChat.tsx:17 -> security`
- `frontend/src/pages/AIChat.tsx:32 -> security`
- `frontend/src/pages/AIChat.tsx:42 -> security`
- `frontend/src/pages/AIChat.tsx:56 -> security`
- `frontend/src/pages/Dashboard.tsx:108 -> security`
- `frontend/src/pages/Dashboard.tsx:109 -> security`
- `frontend/src/pages/Dashboard.tsx:110 -> security`
- `frontend/src/pages/Dashboard.tsx:118 -> security`
- `frontend/src/pages/Dashboard.tsx:143 -> security`
- `frontend/src/pages/Dashboard.tsx:153 -> security`
- `frontend/src/pages/Dashboard.tsx:165 -> security`
- `frontend/src/pages/Dashboard.tsx:166 -> security`

## PHASE 2 — Core Security Scanners

- [PASS] `backend/app/api`
- [PASS] `backend/app/services`
- [PASS] `backend/app/engines`
- [PASS] `frontend/src/pages`
- [PASS] `frontend/src/services`

Relevant implementation references:
- `frontend/src/layouts/Topbar.tsx:14 -> header`
- `frontend/src/layouts/Topbar.tsx:75 -> header`
- `frontend/src/pages/AIChat.tsx:8 -> header`
- `frontend/src/pages/AIChat.tsx:14 -> header`
- `frontend/src/pages/Dashboard.tsx:14 -> header`
- `frontend/src/pages/Dashboard.tsx:107 -> header`
- `frontend/src/pages/Login.tsx:13 -> password`
- `frontend/src/pages/Login.tsx:14 -> password`
- `frontend/src/pages/Login.tsx:22 -> password`
- `frontend/src/pages/Login.tsx:23 -> password`
- `frontend/src/pages/Login.tsx:29 -> password`
- `frontend/src/pages/Login.tsx:71 -> password`
- `frontend/src/pages/Login.tsx:74 -> password`
- `frontend/src/pages/Login.tsx:75 -> password`
- `frontend/src/pages/Login.tsx:76 -> password`
- `frontend/src/pages/NetworkAnalyzer.tsx:13 -> header`
- `frontend/src/pages/NetworkAnalyzer.tsx:160 -> header`
- `frontend/src/pages/Reports.tsx:8 -> header`
- `frontend/src/pages/Reports.tsx:15 -> header`
- `frontend/src/pages/Settings.tsx:8 -> header`
- `frontend/src/pages/Settings.tsx:14 -> header`
- `frontend/src/pages/ThreatIntel.tsx:14 -> header`
- `frontend/src/pages/ThreatIntel.tsx:116 -> header`
- `frontend/src/pages/VulnerabilityScanner.tsx:15 -> header`
- `frontend/src/pages/VulnerabilityScanner.tsx:250 -> header`
- `frontend/src/pages/WebSecurity.tsx:16 -> header`
- `frontend/src/pages/WebSecurity.tsx:21 -> header`
- `frontend/src/pages/WebSecurity.tsx:25 -> header`
- `frontend/src/pages/WebSecurity.tsx:28 -> header`
- `frontend/src/pages/WebSecurity.tsx:197 -> header`

## PHASE 3 — Network Security

- [PASS] `backend/app/api`
- [PASS] `backend/app/services`
- [PASS] `backend/app/engines`
- [PASS] `frontend/src/pages`
- [PASS] `frontend/src/services`

Relevant implementation references:
- `test_network_ws.py:1 -> port`
- `test_network_ws.py:2 -> port`
- `test_network_ws.py:5 -> network`
- `test_network_ws.py:9 -> socket`
- `test_network_ws.py:10 -> socket`
- `test_network_ws.py:13 -> socket`
- `autotest/run_tests.py:1 -> port`
- `autotest/run_tests.py:2 -> port`
- `autotest/run_tests.py:3 -> port`
- `autotest/run_tests.py:74 -> port`
- `autotest/run_tests.py:77 -> port`
- `autotest/run_tests.py:78 -> port`
- `autotest/run_tests.py:87 -> port`
- `autotest/run_tests.py:95 -> port`
- `autotest/run_tests.py:96 -> port`
- `autotest/run_tests.py:149 -> port`
- `autotest/run_tests.py:158 -> port`
- `frontend/eslint.config.js:1 -> port`
- `frontend/eslint.config.js:2 -> port`
- `frontend/eslint.config.js:3 -> port`
- `frontend/eslint.config.js:4 -> port`
- `frontend/eslint.config.js:5 -> port`
- `frontend/eslint.config.js:6 -> port`
- `frontend/eslint.config.js:8 -> port`
- `frontend/package-lock.json:138 -> port`
- `frontend/package-lock.json:140 -> port`
- `frontend/package-lock.json:159 -> port`
- `frontend/package-lock.json:444 -> port`
- `frontend/package-lock.json:446 -> port`
- `frontend/package-lock.json:1745 -> nmap`

## PHASE 4 — Vulnerability Detection

- [PASS] `backend/app/api`
- [PASS] `backend/app/services`
- [PASS] `backend/app/engines`
- [PASS] `frontend/src/pages`
- [PASS] `frontend/src/services`

Relevant implementation references:
- `frontend/package-lock.json:1296 -> cve`
- `frontend/package-lock.json:3740 -> cve`
- `frontend/src/App.tsx:11 -> vulnerability`
- `frontend/src/App.tsx:44 -> vulnerability`
- `frontend/src/layouts/Sidebar.tsx:32 -> vulnerability`
- `frontend/src/pages/AIChat.tsx:17 -> cve`
- `frontend/src/pages/AIChat.tsx:46 -> cve`
- `frontend/src/pages/Dashboard.tsx:110 -> vulnerability`
- `frontend/src/pages/Dashboard.tsx:189 -> vulnerability`
- `frontend/src/pages/Dashboard.tsx:190 -> finding`
- `frontend/src/pages/Dashboard.tsx:192 -> vulnerability`
- `frontend/src/pages/Dashboard.tsx:299 -> vulnerability`
- `frontend/src/pages/Dashboard.tsx:305 -> vulnerability`
- `frontend/src/pages/Dashboard.tsx:309 -> vulnerability`
- `frontend/src/pages/Dashboard.tsx:329 -> finding`
- `frontend/src/pages/Dashboard.tsx:333 -> vulnerability`
- `frontend/src/pages/VulnerabilityScanner.tsx:18 -> vulnerability`
- `frontend/src/pages/VulnerabilityScanner.tsx:19 -> vulnerability`
- `frontend/src/pages/VulnerabilityScanner.tsx:20 -> vulnerability`
- `frontend/src/pages/VulnerabilityScanner.tsx:22 -> vulnerability`
- `frontend/src/pages/VulnerabilityScanner.tsx:26 -> vulnerability`
- `frontend/src/pages/VulnerabilityScanner.tsx:50 -> vulnerability`
- `frontend/src/pages/VulnerabilityScanner.tsx:68 -> vulnerability`
- `frontend/src/pages/VulnerabilityScanner.tsx:75 -> vulnerability`
- `frontend/src/pages/VulnerabilityScanner.tsx:84 -> finding`
- `frontend/src/pages/VulnerabilityScanner.tsx:85 -> vulnerability`
- `frontend/src/pages/VulnerabilityScanner.tsx:111 -> finding`
- `frontend/src/pages/VulnerabilityScanner.tsx:127 -> finding`
- `frontend/src/pages/VulnerabilityScanner.tsx:135 -> finding`
- `frontend/src/pages/VulnerabilityScanner.tsx:156 -> vulnerability`

## PHASE 5 — File Integrity & Monitoring

- [PASS] `backend/app/api`
- [PASS] `backend/app/services`
- [PASS] `backend/app/engines`
- [PASS] `frontend/src/pages`
- [PASS] `frontend/src/services`

Relevant implementation references:
- `autotest/run_tests.py:6 -> file`
- `frontend/eslint.config.js:11 -> file`
- `frontend/package-lock.json:4 -> file`
- `frontend/package-lock.json:41 -> integrity`
- `frontend/package-lock.json:56 -> integrity`
- `frontend/package-lock.json:66 -> integrity`
- `frontend/package-lock.json:97 -> integrity`
- `frontend/package-lock.json:114 -> integrity`
- `frontend/package-lock.json:131 -> integrity`
- `frontend/package-lock.json:141 -> integrity`
- `frontend/package-lock.json:155 -> integrity`
- `frontend/package-lock.json:173 -> integrity`
- `frontend/package-lock.json:183 -> integrity`
- `frontend/package-lock.json:193 -> integrity`
- `frontend/package-lock.json:203 -> integrity`
- `frontend/package-lock.json:217 -> integrity`
- `frontend/package-lock.json:233 -> integrity`
- `frontend/package-lock.json:248 -> integrity`
- `frontend/package-lock.json:267 -> integrity`
- `frontend/package-lock.json:281 -> integrity`
- `frontend/package-lock.json:300 -> integrity`
- `frontend/package-lock.json:313 -> integrity`
- `frontend/package-lock.json:323 -> integrity`
- `frontend/package-lock.json:338 -> integrity`
- `frontend/package-lock.json:351 -> integrity`
- `frontend/package-lock.json:364 -> integrity`
- `frontend/package-lock.json:385 -> integrity`
- `frontend/package-lock.json:395 -> integrity`
- `frontend/package-lock.json:409 -> integrity`
- `frontend/package-lock.json:422 -> integrity`

## PHASE 6 — Security Dashboard & Integration

- [PASS] `backend/app/api`
- [PASS] `backend/app/services`
- [PASS] `backend/app/crud`
- [PASS] `backend/app/models`
- [PASS] `backend/app/schemas`
- [PASS] `frontend/src/pages`
- [PASS] `frontend/src/hooks`
- [PASS] `frontend/src/services`
- [PASS] `frontend/src/types`

Relevant implementation references:
- `autotest/run_tests.py:92 -> scan`
- `autotest/run_tests.py:95 -> scan`
- `autotest/run_tests.py:96 -> scan`
- `frontend/src/App.tsx:8 -> dashboard`
- `frontend/src/App.tsx:11 -> scan`
- `frontend/src/App.tsx:35 -> dashboard`
- `frontend/src/App.tsx:36 -> dashboard`
- `frontend/src/App.tsx:44 -> scan`
- `frontend/src/App.tsx:75 -> dashboard`
- `frontend/src/App.tsx:80 -> dashboard`
- `frontend/tests/routes.spec.ts:5 -> dashboard`
- `frontend/src/hooks/useDashboard.ts:2 -> dashboard`
- `frontend/src/hooks/useDashboard.ts:4 -> dashboard`
- `frontend/src/hooks/useDashboard.ts:6 -> dashboard`
- `frontend/src/hooks/useDashboard.ts:8 -> dashboard`
- `frontend/src/hooks/useNetworkWebSocket.ts:3 -> statistics`
- `frontend/src/hooks/useNetworkWebSocket.ts:5 -> statistics`
- `frontend/src/hooks/useNetworkWebSocket.ts:16 -> statistics`
- `frontend/src/hooks/useNetworkWebSocket.ts:20 -> statistics`
- `frontend/src/hooks/useNetworkWebSocket.ts:21 -> statistics`
- `frontend/src/hooks/useNetworkWebSocket.ts:49 -> statistics`
- `frontend/src/layouts/DashboardLayout.tsx:5 -> dashboard`
- `frontend/src/layouts/DashboardLayout.tsx:9 -> dashboard`
- `frontend/src/layouts/DashboardLayout.tsx:11 -> dashboard`
- `frontend/src/layouts/Sidebar.tsx:6 -> dashboard`
- `frontend/src/layouts/Sidebar.tsx:9 -> scan`
- `frontend/src/layouts/Sidebar.tsx:22 -> dashboard`
- `frontend/src/layouts/Sidebar.tsx:23 -> dashboard`
- `frontend/src/layouts/Sidebar.tsx:24 -> dashboard`
- `frontend/src/layouts/Sidebar.tsx:32 -> scan`

## PHASE 7 — Scan History / Master Scan

- [PASS] `backend/app/api/master_scan.py`
- [PASS] `backend/app/services/master_scan_service.py`
- [PASS] `backend/app/crud/master_scan.py`
- [PASS] `backend/app/models/master_scan.py`
- [PASS] `backend/app/models/scan.py`
- [PASS] `backend/app/schemas/master_scan.py`
- [PASS] `frontend/src/pages/Dashboard.tsx`

Relevant implementation references:
- `autotest/run_tests.py:96 -> master_scan`
- `backend/app/main.py:7 -> master_scan`
- `backend/app/main.py:42 -> master_scan`
- `backend/tests/test_api.py:84 -> master_scan`
- `backend/tests/test_api.py:98 -> master_scan`
- `backend/tests/test_api.py:119 -> master_scan`
- `backend/tests/test_api.py:142 -> master_scan`
- `backend/tests/test_api.py:165 -> master_scan`
- `backend/tests/test_api.py:193 -> master_scan`
- `backend/tests/test_api.py:218 -> master_scan`
- `backend/tests/test_api.py:243 -> master_scan`
- `backend/tests/test_api.py:266 -> master_scan`
- `backend/tests/test_api.py:296 -> master_scan`
- `backend/tests/test_api.py:315 -> master_scan`
- `backend/tests/test_api.py:338 -> master_scan`
- `backend/tests/test_api.py:362 -> master_scan`
- `backend/tests/test_api.py:383 -> master_scan`
- `backend/tests/test_api.py:404 -> master_scan`
- `backend/tests/test_api.py:412 -> master_scan`
- `backend/tests/test_api.py:436 -> master_scan`
- `backend/tests/test_api.py:462 -> master_scan`
- `backend/tests/test_api.py:480 -> master_scan`
- `backend/tests/test_api.py:523 -> master_scan`
- `backend/tests/test_api.py:545 -> master_scan`
- `backend/tests/test_api.py:553 -> master_scan`
- `backend/tests/test_api.py:571 -> master_scan`
- `backend/tests/test_api.py:587 -> master_scan`
- `backend/tests/test_api.py:599 -> master_scan`
- `backend/tests/test_api.py:611 -> master_scan`
- `backend/tests/test_api.py:658 -> master_scan`

## PHASE 8 — Security Reports

- [PASS] `backend/app/api/reports.py`
- [PASS] `backend/app/services/report_service.py`
- [PASS] `backend/app/reports`
- [PASS] `frontend/src/pages/Reports.tsx`

Relevant implementation references:
- `autotest/run_tests.py:129 -> json`
- `autotest/run_tests.py:131 -> json`
- `autotest/run_tests.py:143 -> json`
- `autotest/run_tests.py:149 -> report`
- `autotest/run_tests.py:158 -> report`
- `frontend/package-lock.json:83 -> json`
- `frontend/package-lock.json:355 -> json`
- `frontend/package-lock.json:1186 -> json`
- `frontend/package-lock.json:1188 -> json`
- `frontend/package-lock.json:1545 -> json`
- `frontend/package-lock.json:1546 -> json`
- `frontend/package-lock.json:2058 -> json`
- `frontend/package-lock.json:2220 -> json`
- `frontend/package-lock.json:2222 -> json`
- `frontend/package-lock.json:2620 -> json`
- `frontend/package-lock.json:2622 -> json`
- `frontend/package-lock.json:2623 -> pdf`
- `frontend/package-lock.json:2627 -> json`
- `frontend/package-lock.json:2629 -> json`
- `frontend/package-lock.json:2634 -> json`
- `frontend/package-lock.json:2636 -> json`
- `frontend/package-lock.json:2641 -> json`
- `frontend/package-lock.json:2643 -> json`
- `frontend/package-lock.json:2648 -> json`
- `frontend/package-lock.json:2661 -> json`
- `frontend/tsconfig.json:4 -> json`
- `frontend/tsconfig.json:5 -> json`
- `frontend/src/App.tsx:15 -> report`
- `frontend/src/App.tsx:59 -> report`
- `frontend/src/App.tsx:60 -> report`

## PHASE 9 — AI Security Assistant

- [PASS] `backend/app`
- [PASS] `frontend/src/pages/AIChat.tsx`
- [PASS] `frontend/src/services`
- [PASS] `frontend/src/types`

Relevant implementation references:
- `test_network_ws.py:13 -> ai`
- `autotest/run_tests.py:35 -> ai`
- `autotest/run_tests.py:43 -> ai`
- `autotest/run_tests.py:47 -> ai`
- `autotest/run_tests.py:61 -> ai`
- `autotest/run_tests.py:74 -> ai`
- `autotest/run_tests.py:77 -> ai`
- `autotest/run_tests.py:78 -> ai`
- `autotest/run_tests.py:87 -> ai`
- `autotest/run_tests.py:154 -> ai`
- `autotest/run_tests.py:163 -> ai`
- `autotest/run_tests.py:167 -> ai`
- `autotest/run_tests.py:169 -> ai`
- `autotest/run_tests.py:173 -> ai`
- `autotest/run_tests.py:174 -> ai`
- `autotest/run_tests.py:180 -> ai`
- `autotest/run_tests.py:181 -> ai`
- `frontend/package-lock.json:11 -> ai`
- `frontend/package-lock.json:19 -> ai`
- `frontend/package-lock.json:66 -> ai`
- `frontend/package-lock.json:267 -> llm`
- `frontend/package-lock.json:437 -> ai`
- `frontend/package-lock.json:504 -> ai`
- `frontend/package-lock.json:826 -> ai`
- `frontend/package-lock.json:828 -> ai`
- `frontend/package-lock.json:838 -> ai`
- `frontend/package-lock.json:841 -> ai`
- `frontend/package-lock.json:843 -> ai`
- `frontend/package-lock.json:844 -> ai`
- `frontend/package-lock.json:850 -> ai`

## PHASE 10 — Alerts / Threat Intelligence

- [PASS] `backend/app`
- [PASS] `frontend/src/pages/ThreatIntel.tsx`
- [PASS] `frontend/src/services`
- [PASS] `frontend/src/types`

Relevant implementation references:
- `frontend/src/App.tsx:13 -> threat`
- `frontend/src/App.tsx:51 -> threat`
- `frontend/src/App.tsx:52 -> threat`
- `frontend/tests/routes.spec.ts:9 -> threat`
- `frontend/src/layouts/Sidebar.tsx:47 -> threat`
- `frontend/src/layouts/Sidebar.tsx:49 -> threat`
- `frontend/src/layouts/Topbar.tsx:50 -> notification`
- `frontend/src/pages/Dashboard.tsx:4 -> alert`
- `frontend/src/pages/Dashboard.tsx:9 -> alert`
- `frontend/src/pages/Dashboard.tsx:110 -> threat`
- `frontend/src/pages/Dashboard.tsx:126 -> alert`
- `frontend/src/pages/Dashboard.tsx:172 -> threat`
- `frontend/src/pages/Dashboard.tsx:173 -> threat`
- `frontend/src/pages/Dashboard.tsx:174 -> threat`
- `frontend/src/pages/Dashboard.tsx:175 -> alert`
- `frontend/src/pages/Dashboard.tsx:176 -> threat`
- `frontend/src/pages/Dashboard.tsx:180 -> alert`
- `frontend/src/pages/Dashboard.tsx:181 -> alert`
- `frontend/src/pages/Dashboard.tsx:183 -> alert`
- `frontend/src/pages/Dashboard.tsx:184 -> alert`
- `frontend/src/pages/NetworkAnalyzer.tsx:8 -> alert`
- `frontend/src/pages/NetworkAnalyzer.tsx:267 -> alert`
- `frontend/src/pages/Settings.tsx:26 -> alert`
- `frontend/src/pages/ThreatIntel.tsx:9 -> alert`
- `frontend/src/pages/ThreatIntel.tsx:16 -> threat`
- `frontend/src/pages/ThreatIntel.tsx:20 -> threat`
- `frontend/src/pages/ThreatIntel.tsx:21 -> threat`
- `frontend/src/pages/ThreatIntel.tsx:26 -> threat`
- `frontend/src/pages/ThreatIntel.tsx:29 -> threat`
- `frontend/src/pages/ThreatIntel.tsx:69 -> threat`

## PHASE 11 — Dashboard

- [PASS] `backend/app`
- [PASS] `frontend/src/pages/Dashboard.tsx`
- [PASS] `frontend/src/hooks`
- [PASS] `frontend/src/services`
- [PASS] `frontend/src/types`

Relevant implementation references:
- `frontend/src/App.tsx:8 -> dashboard`
- `frontend/src/App.tsx:35 -> dashboard`
- `frontend/src/App.tsx:36 -> dashboard`
- `frontend/src/App.tsx:75 -> dashboard`
- `frontend/src/App.tsx:80 -> dashboard`
- `frontend/tests/routes.spec.ts:5 -> dashboard`
- `frontend/src/hooks/useDashboard.ts:2 -> dashboard`
- `frontend/src/hooks/useDashboard.ts:4 -> dashboard`
- `frontend/src/hooks/useDashboard.ts:6 -> dashboard`
- `frontend/src/hooks/useDashboard.ts:8 -> dashboard`
- `frontend/src/layouts/DashboardLayout.tsx:5 -> dashboard`
- `frontend/src/layouts/DashboardLayout.tsx:9 -> dashboard`
- `frontend/src/layouts/DashboardLayout.tsx:11 -> dashboard`
- `frontend/src/layouts/Sidebar.tsx:6 -> dashboard`
- `frontend/src/layouts/Sidebar.tsx:22 -> dashboard`
- `frontend/src/layouts/Sidebar.tsx:23 -> dashboard`
- `frontend/src/layouts/Sidebar.tsx:24 -> dashboard`
- `frontend/src/pages/AIChat.tsx:7 -> dashboard`
- `frontend/src/pages/AIChat.tsx:12 -> dashboard`
- `frontend/src/pages/AIChat.tsx:70 -> dashboard`
- `frontend/src/pages/Dashboard.tsx:13 -> dashboard`
- `frontend/src/pages/Dashboard.tsx:16 -> dashboard`
- `frontend/src/pages/Dashboard.tsx:17 -> dashboard`
- `frontend/src/pages/Dashboard.tsx:18 -> dashboard`
- `frontend/src/pages/Dashboard.tsx:60 -> dashboard`
- `frontend/src/pages/Dashboard.tsx:62 -> dashboard`
- `frontend/src/pages/Dashboard.tsx:73 -> dashboard`
- `frontend/src/pages/Dashboard.tsx:79 -> dashboard`
- `frontend/src/pages/Dashboard.tsx:97 -> dashboard`
- `frontend/src/pages/Dashboard.tsx:105 -> dashboard`

## PHASE 12 — Database / Migrations

- [PASS] `backend/app/database`
- [PASS] `backend/app/models`
- [PASS] `backend/app/schemas`
- [PASS] `backend/app/crud`
- [PASS] `backend/alembic`

Relevant implementation references:
- `frontend/src/types/dashboard.ts:56 -> created_at`
- `frontend/src/types/fileIntegrity.ts:8 -> created_at`
- `frontend/src/pages/security/FileIntegrity.tsx:163 -> created_at`
- `frontend/src/pages/security/FileIntegrity.tsx:170 -> created_at`
- `backend/alembic/env.py:11 -> DATABASE_URL`
- `backend/alembic/env.py:21 -> DATABASE_URL`
- `backend/tests/conftest.py:6 -> DATABASE_URL`
- `backend/tests/test_api.py:289 -> created_at`
- `backend/tests/test_api.py:498 -> created_at`
- `backend/tests/test_api.py:651 -> created_at`
- `backend/app/api/master_scan.py:70 -> created_at`
- `backend/app/api/master_scan.py:109 -> created_at`
- `backend/app/core/config.py:12 -> DATABASE_URL`
- `backend/app/core/config.py:14 -> DATABASE_URL`
- `backend/app/core/config.py:35 -> DATABASE_URL`
- `backend/app/core/config.py:48 -> DATABASE_URL`
- `backend/app/core/config.py:54 -> DATABASE_URL`
- `backend/app/core/config.py:55 -> DATABASE_URL`
- `backend/app/core/config.py:56 -> DATABASE_URL`
- `backend/app/crud/master_scan.py:37 -> created_at`
- `backend/app/database/database.py:8 -> DATABASE_URL`
- `backend/app/database/database.py:11 -> DATABASE_URL`
- `backend/app/database/database.py:14 -> DATABASE_URL`
- `backend/app/models/alert.py:1 -> ForeignKey`
- `backend/app/models/alert.py:2 -> relationship`
- `backend/app/models/alert.py:19 -> ForeignKey`
- `backend/app/models/alert.py:43 -> created_at`
- `backend/app/models/alert.py:48 -> relationship`
- `backend/app/models/chat_history.py:1 -> ForeignKey`
- `backend/app/models/chat_history.py:2 -> relationship`

## PHASE 13 — Zero Trust / Passwordless

- [PASS] `backend/app`
- [PASS] `frontend/src`

Relevant implementation references:
- `frontend/src/pages/NetworkAnalyzer.tsx:244 -> session`
- `frontend/src/pages/Settings.tsx:32 -> session`
- `frontend/src/services/websocket.ts:21 -> session`
- `backend/tests/conftest.py:12 -> session`
- `backend/tests/conftest.py:22 -> session`
- `backend/tests/test_authorization_boundaries.py:7 -> session`
- `backend/tests/test_authorization_boundaries.py:81 -> session`
- `backend/app/api/alert.py:2 -> session`
- `backend/app/api/alert.py:16 -> session`
- `backend/app/api/alert.py:24 -> session`
- `backend/app/api/auth.py:2 -> session`
- `backend/app/api/auth.py:31 -> session`
- `backend/app/api/auth.py:45 -> session`
- `backend/app/api/dashboard.py:2 -> session`
- `backend/app/api/dashboard.py:23 -> session`
- `backend/app/api/dashboard.py:36 -> session`
- `backend/app/api/dependencies.py:3 -> session`
- `backend/app/api/dependencies.py:13 -> session`
- `backend/app/api/file_integrity.py:2 -> session`
- `backend/app/api/file_integrity.py:15 -> session`
- `backend/app/api/master_scan.py:2 -> session`
- `backend/app/api/master_scan.py:31 -> session`
- `backend/app/api/master_scan.py:53 -> session`
- `backend/app/api/master_scan.py:80 -> session`
- `backend/app/api/network_scan.py:7 -> session`
- `backend/app/api/network_scan.py:23 -> session`
- `backend/app/api/phishing.py:7 -> session`
- `backend/app/api/phishing.py:23 -> session`
- `backend/app/api/reports.py:3 -> session`
- `backend/app/api/reports.py:16 -> session`

## PHASE 14 — Testing

- [PASS] `backend/tests`
- [PASS] `autotest`
- [PASS] `frontend/tests`
- [PASS] `frontend`

Relevant implementation references:
- `test_network_ws.py:2 -> websocket`
- `test_network_ws.py:9 -> websocket`
- `test_network_ws.py:10 -> websocket`
- `test_network_ws.py:13 -> websocket`
- `frontend/package-lock.json:24 -> playwright`
- `frontend/package-lock.json:526 -> playwright`
- `frontend/package-lock.json:528 -> playwright`
- `frontend/package-lock.json:533 -> playwright`
- `frontend/package-lock.json:536 -> playwright`
- `frontend/package-lock.json:3146 -> playwright`
- `frontend/package-lock.json:3148 -> playwright`
- `frontend/package-lock.json:3153 -> playwright`
- `frontend/package-lock.json:3156 -> playwright`
- `frontend/package-lock.json:3165 -> playwright`
- `frontend/package-lock.json:3167 -> playwright`
- `frontend/package-lock.json:3172 -> playwright`
- `frontend/package.json:26 -> playwright`
- `frontend/playwright.config.ts:1 -> playwright`
- `frontend/tests/routes.spec.ts:1 -> playwright`
- `frontend/src/hooks/useNetworkWebSocket.ts:2 -> websocket`
- `frontend/src/hooks/useNetworkWebSocket.ts:12 -> websocket`
- `frontend/src/hooks/useNetworkWebSocket.ts:13 -> websocket`
- `frontend/src/hooks/useNetworkWebSocket.ts:26 -> websocket`
- `frontend/src/hooks/useNetworkWebSocket.ts:27 -> websocket`
- `frontend/src/hooks/useNetworkWebSocket.ts:29 -> websocket`
- `frontend/src/hooks/useNetworkWebSocket.ts:36 -> websocket`
- `frontend/src/pages/Login.tsx:37 -> authentication`
- `frontend/src/pages/Login.tsx:84 -> authentication`
- `frontend/src/pages/NetworkAnalyzer.tsx:21 -> websocket`
- `frontend/src/pages/NetworkAnalyzer.tsx:22 -> websocket`

## PHASE 15 — Final SOC UI/UX

- [PASS] `frontend/src/layouts`
- [PASS] `frontend/src/pages`
- [PASS] `frontend/src/components`
- [PASS] `frontend/src/assets`

Relevant implementation references:
- `frontend/src/App.tsx:8 -> Dashboard`
- `frontend/src/App.tsx:10 -> NetworkAnalyzer`
- `frontend/src/App.tsx:11 -> VulnerabilityScanner`
- `frontend/src/App.tsx:12 -> WebSecurity`
- `frontend/src/App.tsx:13 -> ThreatIntel`
- `frontend/src/App.tsx:14 -> AIChat`
- `frontend/src/App.tsx:15 -> Reports`
- `frontend/src/App.tsx:16 -> Settings`
- `frontend/src/App.tsx:35 -> Dashboard`
- `frontend/src/App.tsx:36 -> Dashboard`
- `frontend/src/App.tsx:40 -> NetworkAnalyzer`
- `frontend/src/App.tsx:44 -> VulnerabilityScanner`
- `frontend/src/App.tsx:48 -> WebSecurity`
- `frontend/src/App.tsx:52 -> ThreatIntel`
- `frontend/src/App.tsx:56 -> AIChat`
- `frontend/src/App.tsx:59 -> Reports`
- `frontend/src/App.tsx:60 -> Reports`
- `frontend/src/App.tsx:63 -> Settings`
- `frontend/src/App.tsx:64 -> Settings`
- `frontend/src/App.tsx:75 -> Dashboard`
- `frontend/src/App.tsx:80 -> Dashboard`
- `frontend/tests/routes.spec.ts:5 -> Dashboard`
- `frontend/tests/routes.spec.ts:11 -> Reports`
- `frontend/tests/routes.spec.ts:12 -> Settings`
- `frontend/src/hooks/useDashboard.ts:2 -> Dashboard`
- `frontend/src/hooks/useDashboard.ts:4 -> Dashboard`
- `frontend/src/hooks/useDashboard.ts:6 -> Dashboard`
- `frontend/src/hooks/useDashboard.ts:8 -> Dashboard`
- `frontend/src/layouts/DashboardLayout.tsx:5 -> Dashboard`
- `frontend/src/layouts/DashboardLayout.tsx:9 -> Dashboard`

## OBJECTIVE TESTS

- [PASS] `C:\Users\91704\Desktop\CyberShield AI v2\CyberShield AI\backend\.venv\Scripts\python.exe -m compileall -q app`
- [FAIL] `C:\Users\91704\Desktop\CyberShield AI v2\CyberShield AI\backend\.venv\Scripts\python.exe -m pytest -q`
```text
============================= test session starts =============================
platform win32 -- Python 3.13.5, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\91704\Desktop\CyberShield AI v2\CyberShield AI\backend
configfile: pytest.ini
testpaths: tests
plugins: anyio-4.15.1
collected 3 items / 3 errors

=================================== ERRORS ====================================
_____________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module 'C:\Users\91704\Desktop\CyberShield AI v2\CyberShield AI\backend\tests\test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
..\..\..\..\AppData\Local\Programs\Python\Python313\Lib\importlib\__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests\test_api.py:6: in <module>
    from app.main import app
app\main.py:3: in <module>
    from app.api.alert import router as alert_router
app\api\__init__.py:2: in <module>
    from app.api.dashboard import router as dashboard_router
app\api\dashboard.py:7: in <module>
    from app.services.dashboard_service import (
app\services\dashboard_service.py:8: in <module>
    from app.services.network_monitor_service import get_network_snapshot
app\services\network_monitor_service.py:6: in <module>
    from app.services.network_telemetry import get_network_telemetry
app\services\network_telemetry.py:5: in <module>
    import psutil
E   ModuleNotFoundError: No module named 'psutil'
_____________________ ERROR collecting tests/test_auth.py _____________________
ImportError while importing test module 'C:\Users\91704\Desktop\CyberShield AI v2\CyberShield AI\backend\tests\test_auth.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
..\..\..\..\AppData\Local\Programs\Python\Python313\Lib\importlib\__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests\test_auth.py:5: in <module>
    from app.main import app
app\main.py:3: in <module>
    from app.api.alert import router as alert_router
app\api\__init__.py:2: in <module>
    from app.api.dashboard import router as dashboard_router
app\api\dashboard.py:7: in <module>
    from app.services.dashboard_service import (
app\services\dashboard_service.py:8: in <module>
    from app.services.network_monitor_service import get_network_snapshot
app\services\network_monitor_service.py:6: in <module>
    from app.services.network_telemetry import get_network_telemetry
app\services\network_telemetry.py:5: in <module>
    import psutil
E   ModuleNotFoundError: No module named 'psutil'
___________ ERROR collecting tests/test_authorization_boundaries.py ___________
ImportError while importing test module 'C:\Users\91704\Desktop\CyberShield AI v2\CyberShield AI\backend\tests\test_authorization_boundaries.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
..\..\..\..\AppData\Local\Programs\Python\Python313\Lib\importlib\__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests\test_authorization_boundaries.py:8: in <module>
    from app.main import app
app\main.py:3: in <module>
    from app.api.alert import router as alert_router
app\api\__init__.py:2: in <module>
    from app.api.dashboard import router as dashboard_router
app\api\dashboard.py:7: in <module>
    from app.services.dashboard_service import (
app\services\dashboard_service.py:8: in <module>
    from app.services.network_monitor_service import get_network_snapshot
app\services\network_monitor_service.py:6: in <module>
    from app.services.network_telemetry import get_network_telemetry
app\services\network_telemetry.py:5: in <module>
    import psutil
E   ModuleNotFoundError: No module named 'psutil'
============================== warnings summary ===============================
.venv\Lib\site-packages\starlette\testclient.py:53
  C:\Users\91704\Desktop\CyberShield AI v2\CyberShield AI\backend\.venv\Lib\site-packages\starlette\testclient.py:53: DeprecationWarning: The anyio.abc.BlockingPortal alias is deprecated, use anyio.from_thread.BlockingPortal instead.
    _PortalFactoryType = Callable[[], AbstractContextManager[anyio.abc.BlockingPortal]]

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== short test summary info ===========================
ERROR tests/test_api.py
ERROR tests/test_auth.py
ERROR tests/test_authorization_boundaries.py
!!!!!!!!!!!!!!!!!!! Interrupted: 3 errors during collection !!!!!!!!!!!!!!!!!!!
======================== 1 warning, 3 errors in 0.89s =========================
```
- [PASS] `C:\Users\91704\Desktop\CyberShield AI v2\CyberShield AI\backend\.venv\Scripts\python.exe -m alembic heads`
- [BLOCKED] `npm run build`
```text
FileNotFoundError(2, 'The system cannot find the file specified', None, 2, None)
```
- [BLOCKED] `npx tsc --noEmit`
```text
FileNotFoundError(2, 'The system cannot find the file specified', None, 2, None)
```
- [BLOCKED] `npx playwright test`
```text
FileNotFoundError(2, 'The system cannot find the file specified', None, 2, None)
```

## PRODUCTION DATA AUDIT

- No configured production-data keyword findings.

## RELEASE NOTE

PASS means only that the configured objective gates passed. It is not a substitute for external penetration testing, dependency review, infrastructure review, or manual security assessment.