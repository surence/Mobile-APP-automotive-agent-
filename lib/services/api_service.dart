import 'dart:convert';
import 'dart:io';

import 'package:http/http.dart' as http;

import '../models/vehicle_model.dart';

class ApiService {
  // Android Emulator
  static const String baseUrl = "http://10.0.1.10:8000";

  // Physical Android Phone
  // Replace with your PC IPv4 address
  // static const String baseUrl = "http://192.168.1.100:8000";

  // ===============================
  // AI Diagnosis
  // ===============================

  static Future<Map<String, dynamic>> diagnoseVehicle(
      VehicleModel vehicle) async {
    try {
      final response = await http
          .post(
            Uri.parse("$baseUrl/diagnose"),
            headers: {
              "Content-Type": "application/json",
            },
            body: jsonEncode(vehicle.toJson()),
          )
          .timeout(
            const Duration(seconds: 60),
          );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      }
  

      return {
        "success": false,
        "message": response.body,
      };
    } catch (e) {
      print(e);
     return {
    "success": false,
    "message": e.toString(),
  };
}
  }

  // ===============================
  // Vehicle Image Analysis
  // ===============================

  static Future<Map<String, dynamic>> analyzeVehicleImage({
    required VehicleModel vehicle,
    required File imageFile,
  }) async {
    try {
      var request = http.MultipartRequest(
        "POST",
        Uri.parse("$baseUrl/analyze-image"),
      );

      request.fields["make"] = vehicle.make;
      request.fields["model"] = vehicle.model;
      request.fields["year"] = vehicle.year;
      request.fields["mileage"] = vehicle.mileage;
      request.fields["symptom_category"] = vehicle.symptomCategory;
      request.fields["symptoms"] = vehicle.symptoms;
      request.fields["obd_code"] = vehicle.obdCode;

      request.files.add(
        await http.MultipartFile.fromPath(
          "image",
          imageFile.path,
        ),
      );

      final streamedResponse = await request.send();

      final response =
          await http.Response.fromStream(streamedResponse);

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      }

      return {
        "success": false,
        "message": response.body,
      };
    } catch (e) {
      return {
        "success": false,
        "message": e.toString(),
      };
    }
  }

  // ===============================
  // Generate PDF Report
  // ===============================

  static Future<File?> downloadPdfReport(
      VehicleModel vehicle) async {
    try {
      final response = await http.post(
        Uri.parse("$baseUrl/generate-report"),
        headers: {
          "Content-Type": "application/json",
        },
        body: jsonEncode(vehicle.toJson()),
      );

      if (response.statusCode == 200) {
        final tempDir =
            Directory.systemTemp;

        final pdfFile = File(
          "${tempDir.path}/diagnostic_report.pdf",
        );

        await pdfFile.writeAsBytes(
          response.bodyBytes,
        );

        return pdfFile;
      }

      return null;
    } catch (e) {
      return null;
    }
  }

  // ===============================
  // Health Check
  // ===============================

  static Future<bool> checkServer() async {
    try {
      final response = await http
          .get(
            Uri.parse(baseUrl),
          )
          .timeout(
            const Duration(seconds: 5),
          );

      return response.statusCode == 200;
    } catch (_) {
      return false;
    }
  }
}