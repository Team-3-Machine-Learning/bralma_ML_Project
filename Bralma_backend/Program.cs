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

app.MapPost("/predict/ukhousing", (UkHousingRequest request) =>
{
    var prediction = $"Dit is een prediction test :)";

    // Call aws for response

    UkHousingResponse response = new(prediction, PropertyType.D);

    return Results.Ok(response);
})
.WithName("GetUkHousingPrediction");


app.MapPost("/predict/elecdemand", (ElecDemandRequest request) =>
{
    var prediction = $"Dit is een prediction test :)";

    // Call aws for response
    double england_wales_demand = 128;

    ElecDemandResponse response = new(prediction, england_wales_demand);

    return Results.Ok(response);
})
.WithName("GetElecDemandPrediction");

app.Run();
