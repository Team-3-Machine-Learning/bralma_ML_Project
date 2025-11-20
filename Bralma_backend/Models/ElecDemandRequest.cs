namespace Bralma_backend.Models;

public record class ElecDemandRequest
{
    public DateTime SettlementDate { get; init; }
    public int SettlementPeriod { get; init; }
    public double EmbeddedWindGeneration { get; init; }
    public double EmbeddedWindCapacity { get; init; }
    public double EmbeddedSolarGeneration { get; init; }
    public double EmbeddedSolarCapacity { get; init; }
    public double NonBmStor { get; init; }
    public double PumpStoragePumping { get; init; }
    public double Ifa2Flow { get; init; }
    public double BritnedFlow { get; init; }
    public double MoyleFlow { get; init; }
    public double EastWestFlow { get; init; }
    public double NemoFlow { get; init; }
    public int Year { get; init; }

    public ElecDemandRequest(
        DateTime settlementDate,
        int settlementPeriod,
        double embeddedWindGeneration,
        double embeddedWindCapacity,
        double embeddedSolarGeneration,
        double embeddedSolarCapacity,
        double nonBmStor,
        double pumpStoragePumping,
        double ifa2Flow,
        double britnedFlow,
        double moyleFlow,
        double eastWestFlow,
        double nemoFlow,
        int year)
    {
        SettlementDate = settlementDate;
        SettlementPeriod = settlementPeriod;
        EmbeddedWindGeneration = embeddedWindGeneration;
        EmbeddedWindCapacity = embeddedWindCapacity;
        EmbeddedSolarGeneration = embeddedSolarGeneration;
        EmbeddedSolarCapacity = embeddedSolarCapacity;
        NonBmStor = nonBmStor;
        PumpStoragePumping = pumpStoragePumping;
        Ifa2Flow = ifa2Flow;
        BritnedFlow = britnedFlow;
        MoyleFlow = moyleFlow;
        EastWestFlow = eastWestFlow;
        NemoFlow = nemoFlow;
        Year = year;
    }
}
