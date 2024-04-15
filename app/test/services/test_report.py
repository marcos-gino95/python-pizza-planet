import pytest
from seeds.seeder import DataBaseSeeder

def test_get_reports(client, report_uri):
    DataBaseSeeder().run()
    response = client.get(report_uri)
    pytest.assume(response.status.startswith("200"))
