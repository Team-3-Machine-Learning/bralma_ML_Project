using System.Text.Json.Serialization;

namespace Bralma_backend.Models;

public record class ElecDemandRequest
{
    [JsonPropertyName("settlement_date")]
    public DateTime SettlementDate { get; init; }

    [JsonPropertyName("settlement_period")]
    public int SettlementPeriod { get; init; }

    [JsonPropertyName("embedded_wind_generation")]
    public double EmbeddedWindGeneration { get; init; }

    [JsonPropertyName("embedded_wind_capacity")]
    public double EmbeddedWindCapacity { get; init; }

    [JsonPropertyName("embedded_solar_generation")]
    public double EmbeddedSolarGeneration { get; init; }

    [JsonPropertyName("embedded_solar_capacity")]
    public double EmbeddedSolarCapacity { get; init; }

    [JsonPropertyName("non_bm_stor")]
    public double NonBmStor { get; init; }

    [JsonPropertyName("pump_storage_pumping")]
    public double PumpStoragePumping { get; init; }

    [JsonPropertyName("ifa2_flow")]
    public double Ifa2Flow { get; init; }

    [JsonPropertyName("britned_flow")]
    public double BritnedFlow { get; init; }

    [JsonPropertyName("moyle_flow")]
    public double MoyleFlow { get; init; }

    [JsonPropertyName("east_west_flow")]
    public double EastWestFlow { get; init; }

    [JsonPropertyName("nemo_flow")]
    public double NemoFlow { get; init; }

    [JsonPropertyName("year")]
    public int Year { get; init; }
}