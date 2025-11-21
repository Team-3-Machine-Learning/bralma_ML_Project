namespace Bralma_backend.Models;

public record class ElecDemandResponse
{
    public string Response = "Succes!";
    public double EnglandWalesDemand;

    public ElecDemandResponse(string response, double englandWalesDemand)
    {
        Response = response;
        EnglandWalesDemand = englandWalesDemand;
    }
}
