import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';
import 'package:fluttertoast/fluttertoast.dart';
import 'package:image_picker/image_picker.dart';
import 'package:open_filex/open_filex.dart';

import '../models/vehicle_model.dart';
import '../services/api_service.dart';


class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final _formKey = GlobalKey<FormState>();

  final makeController = TextEditingController();
  final modelController = TextEditingController();
  final yearController = TextEditingController();
  final mileageController = TextEditingController();
  final obdController = TextEditingController();
  final symptomsController = TextEditingController();

  String symptomCategory = "Engine";

  bool loading = false;

  File? selectedImage;

  Map<String, dynamic>? result;

  final ImagePicker picker = ImagePicker();

  final List<String> categories = [
    "Engine",
    "Transmission",
    "Brakes",
    "Cooling System",
    "Electrical",
    "Suspension",
    "Fuel System",
    "Steering",
    "Exhaust",
    "Air Conditioning"
  ];

  @override
  void dispose() {
    makeController.dispose();
    modelController.dispose();
    yearController.dispose();
    mileageController.dispose();
    obdController.dispose();
    symptomsController.dispose();
    super.dispose();
  }

  Future<void> pickImage() async {
    final XFile? image = await picker.pickImage(
      source: ImageSource.gallery,
      imageQuality: 80,
    );

    if (image == null) return;

    setState(() {
      selectedImage = File(image.path);
    });

    Fluttertoast.showToast(
      msg: "Vehicle image selected",
    );
  }

  VehicleModel buildVehicle() {
    return VehicleModel(
      make: makeController.text.trim(),
      model: modelController.text.trim(),
      year: yearController.text.trim(),
      mileage: mileageController.text.trim(),
      symptomCategory: symptomCategory,
      symptoms: symptomsController.text.trim(),
      obdCode: obdController.text.trim(),
    );
  }

  String? requiredValidator(String? value) {
    if (value == null || value.trim().isEmpty) {
      return "Required";
    }

    return null;
  }

  String? yearValidator(String? value) {
    if (value == null || value.isEmpty) {
      return "Enter vehicle year";
    }

    if (value.length != 4) {
      return "Year must contain 4 digits";
    }

    return null;
  }

  String? mileageValidator(String? value) {
    if (value == null || value.isEmpty) {
      return "Enter mileage";
    }

    if (int.tryParse(value) == null) {
      return "Mileage must be numeric";
    }

    return null;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("AI Automotive Assistant"),
      ),
      body: SafeArea(
        child: Form(
          key: _formKey,
          child: ListView(
            padding: const EdgeInsets.all(16),
            children: [

              const SizedBox(height: 10),

              const Text(
                "Vehicle Information",
                style: TextStyle(
                  fontSize: 22,
                  fontWeight: FontWeight.bold,
                ),
              ),

              const SizedBox(height: 20),

              TextFormField(
                controller: makeController,
                validator: requiredValidator,
                decoration: const InputDecoration(
                  labelText: "Vehicle Make",
                  prefixIcon: Icon(Icons.directions_car),
                ),
              ),

              const SizedBox(height: 15),

              TextFormField(
                controller: modelController,
                validator: requiredValidator,
                decoration: const InputDecoration(
                  labelText: "Vehicle Model",
                  prefixIcon: Icon(Icons.car_repair),
                ),
              ),

              const SizedBox(height: 15),

              TextFormField(
                controller: yearController,
                keyboardType: TextInputType.number,
                validator: yearValidator,
                decoration: const InputDecoration(
                  labelText: "Year",
                  prefixIcon: Icon(Icons.calendar_today),
                ),
              ),

              const SizedBox(height: 15),

              TextFormField(
                controller: mileageController,
                keyboardType: TextInputType.number,
                validator: mileageValidator,
                decoration: const InputDecoration(
                  labelText: "Mileage",
                  prefixIcon: Icon(Icons.speed),
                ),
              ),

              const SizedBox(height: 15),

              DropdownButtonFormField<String>(
                value: symptomCategory,
                decoration: const InputDecoration(
                  labelText: "Symptom Category",
                ),
                items: categories
                    .map(
                      (item) => DropdownMenuItem(
                        value: item,
                        child: Text(item),
                      ),
                    )
                    .toList(),
                onChanged: (value) {
                  setState(() {
                    symptomCategory = value!;
                  });
                },
              ),

              const SizedBox(height: 15),

              TextFormField(
                controller: obdController,
                decoration: const InputDecoration(
                  labelText: "OBD-II Code (Optional)",
                  prefixIcon: Icon(Icons.memory),
                ),
              ),

              const SizedBox(height: 15),

              TextFormField(
                controller: symptomsController,
                validator: requiredValidator,
                maxLines: 5,
                decoration: const InputDecoration(
                  labelText: "Describe the symptoms",
                  alignLabelWithHint: true,
                  prefixIcon: Icon(Icons.description),
                ),
              ),

              const SizedBox(height: 20),
                            Card(
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    children: [

                      if (selectedImage != null)
                        ClipRRect(
                          borderRadius: BorderRadius.circular(12),
                          child: Image.file(
                            selectedImage!,
                            height: 220,
                            width: double.infinity,
                            fit: BoxFit.cover,
                          ),
                        )
                      else
                        const Icon(
                          Icons.image,
                          size: 120,
                          color: Colors.grey,
                        ),

                      const SizedBox(height: 15),

                      ElevatedButton.icon(
                        onPressed: pickImage,
                        icon: const Icon(Icons.upload),
                        label: const Text("Upload Vehicle Image"),
                      ),
                    ],
                  ),
                ),
              ),

              const SizedBox(height: 25),

              if (loading)
                const Center(
                  child: SpinKitCircle(
                    color: Colors.blueGrey,
                    size: 60,
                  ),
                )
              else
                ElevatedButton.icon(
                  icon: const Icon(Icons.psychology),
                  label: const Text(
                    "Analyze Vehicle",
                    style: TextStyle(fontSize: 18),
                  ),
                  onPressed: () async {

                    if (!_formKey.currentState!.validate()) {
                      return;
                    }

                    setState(() {
                      loading = true;
                      result = null;
                    });

                    final vehicle = buildVehicle();

                    Map<String, dynamic> response;

                    if (selectedImage != null) {

                      response =
                          await ApiService.analyzeVehicleImage(
                        vehicle: vehicle,
                        imageFile: selectedImage!,
                      );

                    } else {

                      response =
                          await ApiService.diagnoseVehicle(
                        vehicle,
                      );

                    }

                    setState(() {
                      loading = false;
                      result = response;
                    });

                    if (!(response["success"] ?? false)) {

                      Fluttertoast.showToast(
                        msg: response["message"] ??
                            "Diagnosis failed",
                      );

                    }
                  },
                ),

              const SizedBox(height: 15),

              ElevatedButton.icon(
                icon: const Icon(Icons.picture_as_pdf),
                label: const Text("Generate PDF Report"),
                onPressed: () async {

                  if (!_formKey.currentState!.validate()) {
                    return;
                  }

                  setState(() {
                    loading = true;
                  });

                  final pdf =
                      await ApiService.downloadPdfReport(
                    buildVehicle(),
                  );

                  setState(() {
                    loading = false;
                  });

                  if (pdf == null) {

                    Fluttertoast.showToast(
                      msg: "Unable to generate report",
                    );

                    return;

                  }

                  await OpenFilex.open(
                    pdf.path,
                  );

                  Fluttertoast.showToast(
                    msg: "PDF generated successfully",
                  );
                },
              ),

              const SizedBox(height: 25),
                            if (result != null) ...[

                Card(
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      crossAxisAlignment:
                          CrossAxisAlignment.start,
                      children: [

                        const Text(
                          "AI Diagnosis",
                          style: TextStyle(
                            fontSize: 22,
                            fontWeight: FontWeight.bold,
                          ),
                        ),

                        const Divider(),

                        Text(
                          result!["ai_diagnosis"] ??
                              "No diagnosis available.",
                          style: const TextStyle(
                            fontSize: 16,
                          ),
                        ),
                      ],
                    ),
                  ),
                ),

                const SizedBox(height: 20),

                if (result!["damage_analysis"] != null)

                  Card(
                    child: Padding(
                      padding: const EdgeInsets.all(16),
                      child: Column(
                        crossAxisAlignment:
                            CrossAxisAlignment.start,
                        children: [

                          const Text(
                            "Vehicle Damage Analysis",
                            style: TextStyle(
                              fontSize: 20,
                              fontWeight:
                                  FontWeight.bold,
                            ),
                          ),

                          const Divider(),

                          Text(
                            result!["damage_analysis"],
                          ),
                        ],
                      ),
                    ),
                  ),

                const SizedBox(height: 20),

                Card(
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      crossAxisAlignment:
                          CrossAxisAlignment.start,
                      children: [

                        const Text(
                          "Diagnosis Tool",
                          style: TextStyle(
                            fontSize: 20,
                            fontWeight:
                                FontWeight.bold,
                          ),
                        ),

                        const Divider(),

                        Text(
                          result!["tool_results"]
                                  ["diagnosis"] ??
                              "",
                        ),
                      ],
                    ),
                  ),
                ),

                const SizedBox(height: 20),

                Card(
                  child: ListTile(
                    leading: const Icon(
                      Icons.attach_money,
                      color: Colors.green,
                    ),
                    title:
                        const Text("Estimated Repair Cost"),
                    subtitle: Text(
                      result!["tool_results"]
                              ["repair_cost"] ??
                          "",
                    ),
                  ),
                ),

                const SizedBox(height: 15),

                Card(
                  child: ListTile(
                    leading: const Icon(
                      Icons.build_circle,
                      color: Colors.orange,
                    ),
                    title: const Text(
                        "Maintenance Recommendation"),
                    subtitle: Text(
                      result!["tool_results"]
                              ["maintenance"] ??
                          "",
                    ),
                  ),
                ),

                const SizedBox(height: 15),

                Card(
                  child: ListTile(
                    leading: const Icon(
                      Icons.memory,
                      color: Colors.blue,
                    ),
                    title:
                        const Text("OBD-II Analysis"),
                    subtitle: Text(
                      result!["tool_results"]
                              ["obd_analysis"] ??
                          "",
                    ),
                  ),
                ),
              ],

              const SizedBox(height: 30),
            ],
          ),
        ),
      ),
    );
  }
}