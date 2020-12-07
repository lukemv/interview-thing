from spacex.data import SpaceXData


# This test covers enough of the original class methods
# to establish a working baseline
def test_payloads_when_id_1_returns_expected():
  sut = SpaceXData()
  pl = sut.get_payloads(1)
  assert len(pl) == 1
  assert pl[0]["payload_id"] == "FalconSAT-2"
