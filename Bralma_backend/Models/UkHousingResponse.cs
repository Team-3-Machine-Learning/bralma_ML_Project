namespace Bralma_backend.Models
{
    public record class UkHousingResponse
    {
        public string PropertyType;

        public UkHousingResponse(string propertyType)
        {
            PropertyType = propertyType;
        }
    }
}