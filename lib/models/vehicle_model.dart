class VehicleModel{
  final String make;
  final String model;
  final String year;
  final String mileage;
  final String symptomCategory;
  final String symptoms;
  final String obdCode;

  VehicleModel({
    required this.make,
    required this.model,
    required this.year,
    required this.mileage,
    required this.symptomCategory,
    required this.symptoms,
    required this.obdCode,
  });

  Map<String, dynamic> toJson() {
    return {
      "make": make,
      "model": model,
      "year": year,
      "mileage": mileage,
      "symptom_category": symptomCategory,
      "symptoms": symptoms,
      "obd_code": obdCode,
    };
  }

  factory VehicleModel.fromJson(Map<String, dynamic> json) {
    return VehicleModel(
      make: json["make"] ?? "",
      model: json["model"] ?? "",
      year: json["year"] ?? "",
      mileage: json["mileage"] ?? "",
      symptomCategory: json["symptom_category"] ?? "",
      symptoms: json["symptoms"] ?? "",
      obdCode: json["obd_code"] ?? "",
    );
  }

  VehicleModel copyWith({
    String? make,
    String? model,
    String? year,
    String? mileage,
    String? symptomCategory,
    String? symptoms,
    String? obdCode,
  }) {
    return VehicleModel(
      make: make ?? this.make,
      model: model ?? this.model,
      year: year ?? this.year,
      mileage: mileage ?? this.mileage,
      symptomCategory: symptomCategory ?? this.symptomCategory,
      symptoms: symptoms ?? this.symptoms,
      obdCode: obdCode ?? this.obdCode,
    );
  }
}