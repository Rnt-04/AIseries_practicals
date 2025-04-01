using UnityEngine;
using System.Collections.Generic;

public class MapManager : MonoBehaviour
{
    public List<Region> regions; // List of all regions
    private Color[] availableColors = { Color.red, Color.green, Color.blue };

   void Start()
    {
    Invoke(nameof(AssignColors), 0.1f); // Delay to ensure regions initialize
    DrawRegionBorders();
    }


    void AssignColors()
    {
        foreach (Region region in regions)
        {
            HashSet<Color> usedColors = new HashSet<Color>();

            // Check neighboring regions to avoid duplicate colors
            foreach (Region neighbor in region.neighbors)
            {
                usedColors.Add(neighbor.regionColor);
            }

            // Assign the first available color
            foreach (Color color in availableColors)
            {
                if (!usedColors.Contains(color))
                {
                    region.SetColor(color);
                    break;
                }
            }
        }
    }

    void DrawRegionBorders()
    {
        foreach (Region region in regions)
        {
            foreach (Region neighbor in region.neighbors)
            {
                Debug.DrawLine(region.transform.position, neighbor.transform.position, Color.black, 5f);
            }
        }
    }
}