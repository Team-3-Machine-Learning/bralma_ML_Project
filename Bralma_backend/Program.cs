using Bralma_backend.Models;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

builder.Services.Configure<Microsoft.AspNetCore.Http.Json.JsonOptions>(options =>
{
    options.SerializerOptions.IncludeFields = true;
});

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

app.MapPost("/prediction/ukhousing", async (UkHousingRequest request) =>
{
    using var client = new HttpClient();
    var url = "https://bralma-ml-project-ai-ukhousing.onrender.com/predict";

    var response = await client.PostAsJsonAsync(url, request);

    if (!response.IsSuccessStatusCode)
    {
        return Results.Problem("Failed to fetch prediction from ML API Elec Demand!");
    }

    var result = await response.Content.ReadAsStringAsync();

    UkHousingResponse ukHousingResponse = new(result);

    return Results.Ok(ukHousingResponse);
})
.WithName("GetUkHousingPrediction");


app.MapPost("/prediction/elecdemand", async (ElecDemandRequest request) =>
{
    using var client = new HttpClient();
    var url = "https://bralma-ml-project-ai-elec-demand.onrender.com/predict";

    var response = await client.PostAsJsonAsync(url, request);

    if (!response.IsSuccessStatusCode)
    {
        return Results.Problem("Failed to fetch prediction from ML API Elec Demand!");
    }

    var result = await response.Content.ReadAsStringAsync();

    ElecDemandResponse elecDemandResponse = new(result);

    return Results.Ok(elecDemandResponse);
})
.WithName("GetElecDemandPrediction");

app.Run();
