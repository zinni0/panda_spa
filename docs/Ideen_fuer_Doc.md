# 2

Das System wird von einem Mitarbeiter des Panda Spa´s bedient und auch verwaltet. Externe Nutzer gibt es nicht. Die
Kundschaft im Spa sind typisch deutsch und rufen an, bzw. kommen vor Ort um einen Termin zu vereinbaren. Dadurch spart
sich der Panda viel von seinem recht schmalen Budget für in dem Falle ein Login unnötigen Login Mechanismus.

Sicherheit ist daher gegeben, dass das System sich nicht von außen bedienen lässt. Performance ist dadurch auch recht
irrelevant geworden. Sind die Rechner im Spa zu langsam, müsste man nur diese aufrüsten. Dürfte aber nicht passieren, da
die Anwendung sehr klein ist. Fehler sind so mit bedacht, dass der Nutzer die Anwendung nicht zum Abstürzen bringen
dürfte, sofern er nicht versucht, es extern zu brechen.

# 3

Wir haben das ganze System in Layern aufgebaut. Wir haben ein Datenlayer was die Datenbank umfasst. Dann haben wir das
ORM Layer, welches sich um die Datenbank Verwaltung kümmert. Darüber gibt es ein Validierungslayer, welches prüft, dass
keine Invaliden Daten in die DB gelangen können. Darüber liegt ein Service Layer, welches CRUD-Methoden, Factories und
Manager umfasst, welche sich darum kümmern, die Service Logik einzuhalten und die unterliegenden Layer sinnvoll und
Korrekt einzusetzen. Darauf liegt dann schlussendlich ein Frontend Layer. Dieses könnte man aber gegen alles mögliche
Tauschen, sodass man aus der Anwendung bspw. eine API oder ein Konsolen-Tool machen könnte.

- SQLAlchemy -> ORM
- Pydantic -> Validierung
- PyYAML -> laden von Config
- Flask -> Frontend

# 4

Wir haben ein Factory Pattern eingesetzt, was automatisch aus der Config die jeweiligen Behandlungen als Instanz
zurückgibt.