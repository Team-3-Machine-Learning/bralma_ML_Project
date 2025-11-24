using System.Text.Json.Serialization;

namespace Bralma_backend.Models;

public record class ElecDemandRequest
{
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

}