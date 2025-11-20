namespace Bralma_backend.Models
{
    public record class UkHousingRequest
    {
        public int Price { get; init; }
        public DateTime DateOfTransfer { get; init; }
        public OldNew OldNew { get; init; }
        public Duration Duration { get; init; }
        public required string TownCity { get; init; }
        public required string District { get; init; }
        public required string Country { get; init; }
        public PpdcategoryType PpdcategoryType { get; init; }
        public int Year { get; init; }

        public UkHousingRequest(
            int price,
            DateTime dateOfTransfer,
            OldNew oldNew,
            Duration duration,
            string townCity,
            string district,
            string country,
            PpdcategoryType ppdcategoryType,
            int year)
        {
            Price = price;
            DateOfTransfer = dateOfTransfer;
            OldNew = oldNew;
            Duration = duration;
            TownCity = townCity;
            District = district;
            Country = country;
            PpdcategoryType = ppdcategoryType;
            Year = year;
        }
    }

    public enum OldNew
    {
        N,
        Y
    }

    public enum Duration
    {
        L,
        F,
        U
    }

    public enum PpdcategoryType
    {
        A,
        B
    }
}