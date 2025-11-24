using System.Text.Json.Serialization;

namespace Bralma_backend.Models
{
    public record class UkHousingRequest
    {
        [JsonPropertyName("price")]
        public required int Price { get; init; }

        [JsonPropertyName("old/new")]
        public required string OldNew { get; init; }

        [JsonPropertyName("duration")]
        public required string Duration { get; init; }

        [JsonPropertyName("town/city")]
        public required string TownCity { get; init; }

        [JsonPropertyName("district")]
        public required string District { get; init; }

        [JsonPropertyName("county")]
        public required string County { get; init; }
    }
}