document.getElementById('formatForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const modelType = document.getElementById('modelType').value;
    const partsName = document.getElementById('partsName').value;
    const plate = document.getElementById('plate').value;
    const motor = document.getElementById('motor').value;
    const width = document.getElementById('width').value;
    const manufactureMethod = document.getElementById('manufactureMethod').value;
    const modelOrder = modelType === 'Main_Assembly' ? '' : document.getElementById('modelOrder').value;
    const modelVersion = document.getElementById('modelVersion').value;
    const systemType = document.getElementById('type').value;

    if (modelType === 'Part') {
        if (partsName === 'MOTOR' && !motor) {
            alert("You didn't choose Motor.");
            return;
        }

        if (partsName === 'PLATE' && !plate) {
            alert("You didn't choose Plate.");
            return;
        }

        // If Plate is Aluminium, check if width is provided
        if (plate === 'Aluminium' && (!width || width <= 0)) {
            alert("You must provide a valid width for Aluminium plate.");
            return;
        }
    }

    // Construct the format ID
    const formatId = generateFormatId(
        systemType, modelType, modelOrder, modelVersion, partsName, motor, plate, width, manufactureMethod
    );

    // Display the result
    document.getElementById('result').innerText = formatId;
});

function generateFormatId(systemType, modelType, modelOrder, modelVersion, partsName, motor, plate, width, manufactureMethod) {
    const space = "-";
    const cadId = generateCadId(systemType, modelType, modelOrder, modelVersion);

    // Generate formatId based on the parts name and other conditions
    let formatParts = [];
    let manufacture = '';

    if (modelType === 'Main_Assembly') {
        // If it's Main_Assembly, skip partsName and manufactureMethod, and don't add any extra "0" for Main_Assembly
    } else {
        // Process Part Name only if it's not Main_Assembly
        if (partsName === 'PLATE') {
            if (plate === 'Aluminium' && width > 0) {
                formatParts.push(`${partsName}${space}${plate}${space}${width}`);
            } else if (plate !== 'Aluminium') {
                formatParts.push(`${partsName}${space}${plate}`);  // Include plate name without width for non-Aluminium plates
            }
        } else if (partsName === 'MOTOR' && motor) {
            formatParts.push(`${partsName}${space}${motor}`);
        } else if (partsName) {
            formatParts.push(partsName);
        }

        // Only add the Manufacture Method if it's not Sub_Assembly
        if (modelType !== 'Sub_Assembly' && partsName) {
            manufacture = manufactureMethod;
        }
    }

    // Combine parts to create final formatId
    const formatId = cadId + (formatParts.length > 0 ? space + formatParts.join(space) : '') + (manufacture ? space + manufacture : '');

    return formatId;
}

function generateCadId(systemType, modelType, modelOrder, modelVersion) {
    const year = new Date().getFullYear();
    let cadId = year + "-" + systemType + "-";

    // Modify cadId for Sub_Assembly to include the custom pattern
    if (modelType === 'Sub_Assembly') {
        cadId += `${modelOrder}0${modelVersion}`;  // Format as "ModelOrder0ModelVersion" (e.g., 201, 101)
    } else {
        cadId += formatModelOrder(modelOrder);  // Format modelOrder to ensure leading zeros
        cadId += modelVersion;
    }

    return cadId;
}

// Helper function to format modelOrder with leading zeros
function formatModelOrder(modelOrder) {
    return modelOrder.padStart(2, '0');  // Ensure modelOrder is always 2 digits long
}

document.getElementById('modelType').addEventListener('change', updateFieldVisibility);
document.getElementById('partsName').addEventListener('change', updateFieldVisibility);
document.getElementById('plate').addEventListener('change', updateFieldVisibility);

// Update field visibility when the page loads
document.addEventListener('DOMContentLoaded', updateFieldVisibility);

function updateFieldVisibility() {
    const modelType = document.getElementById('modelType').value;
    const partsName = document.getElementById('partsName').value;
    const plate = document.getElementById('plate').value;

    const modelOrderField = document.getElementById('modelOrder').parentElement;
    modelOrderField.style.display = modelType === 'Main_Assembly' ? 'none' : 'block';

    // Hide PartsName if ModelType == Main_Assembly
    document.getElementById('partsName').parentElement.style.display = modelType === 'Main_Assembly' ? 'none' : 'block';

    // Hide Plate if PartsName isn't PLATE
    document.getElementById('plate').parentElement.style.display = partsName === 'PLATE' ? 'block' : 'none';

    // Show motor only if partsName is MOTOR
    document.getElementById('motor').parentElement.style.display = partsName === 'MOTOR' ? 'block' : 'none';

    // Show width input only if plate is Aluminium
    document.getElementById('width').parentElement.style.display = plate === 'Aluminium' ? 'block' : 'none';

    // Hide Manufacture Method if ModelType == Main_Assembly or Sub_Assembly
    document.getElementById('manufactureMethod').parentElement.style.display = modelType === 'Main_Assembly' || modelType === 'Sub_Assembly' || !partsName ? 'none' : 'block';
}
