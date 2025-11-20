namespace Bralma_backend.Models
{
    public record class UkHousingResponse
    {
        public string ResponseMessage = "Succes"!;
        public PropertyType PropertyType;

        public UkHousingResponse(string responseMessage, PropertyType propertyType)
        {
            ResponseMessage = responseMessage;
            PropertyType = propertyType;
        }
    }

    public enum PropertyType
    {
        F,
        D,
        S,
        T,
        O,
    }
}