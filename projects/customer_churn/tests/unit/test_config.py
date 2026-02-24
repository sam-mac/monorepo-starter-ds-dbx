from customer_churn.config import load_config

def test_load_config(tmp_path):
    p = tmp_path / "c.yml"
    p.write_text("env: dev\ncatalog: main\nschema: s\nfeatures_table: t\n", encoding="utf-8")
    cfg = load_config(p)
    assert cfg.catalog == "main"
    assert cfg.schema == "s"
    assert cfg.features_table == "t"
