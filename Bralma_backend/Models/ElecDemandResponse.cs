namespace Bralma_backend.Models;

public record class ElecDemandResponse
{
    public string EnglandWalesDemand;

    public ElecDemandResponse(string englandWalesDemand)
    {
        EnglandWalesDemand = englandWalesDemand;
    }
}
