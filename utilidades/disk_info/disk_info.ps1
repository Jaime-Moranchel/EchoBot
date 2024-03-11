# Array para almacenar los resultados
 $resultados = @()

 Get-WmiObject Win32_DiskDrive | ForEach-Object {
    $disk = $_
    $partitions = "ASSOCIATORS OF " +
                  "{Win32_DiskDrive.DeviceID='$($disk.DeviceID)'} " +
                  "WHERE AssocClass = Win32_DiskDriveToDiskPartition"
    Get-WmiObject -Query $partitions | ForEach-Object {
      $partition = $_
      $drives = "ASSOCIATORS OF " +
                "{Win32_DiskPartition.DeviceID='$($partition.DeviceID)'} " +
                "WHERE AssocClass = Win32_LogicalDiskToPartition"
      Get-WmiObject -Query $drives | ForEach-Object {
        # Crear un objeto personalizado por cada resultado y agregarlo al array
        $resultado = [PSCustomObject]@{
          Disk        = $disk.DeviceID
          DiskSize    = $disk.Size
          DiskModel   = $disk.Model
          Partition   = $partition.Name
          RawSize     = $partition.Size
          DriveLetter = $_.DeviceID
          VolumeName  = $_.VolumeName
          Size        = $_.Size
          FreeSpace   = $_.FreeSpace
        }
        $resultados += $resultado
      }
    }
 }

 # Convertir el array de resultados a formato JSON y guardarlo en un archivo
 $resultados | ConvertTo-Json | Out-File -FilePath ".\drives.json"
