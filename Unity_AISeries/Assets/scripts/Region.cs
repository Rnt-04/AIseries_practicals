using UnityEngine;
using System.Collections.Generic;

[RequireComponent(typeof(LineRenderer))]
public class Region : MonoBehaviour
{
    public List<Region> neighbors; // Neighboring regions
    public Color regionColor;
    private Renderer regionRenderer;
    private LineRenderer lineRenderer;

    void Start()
    {
        regionRenderer = GetComponent<Renderer>();
        lineRenderer = GetComponent<LineRenderer>();
        lineRenderer.positionCount = 0; // No lines initially
        lineRenderer.startWidth = 0.05f;
        lineRenderer.endWidth = 0.05f;
        lineRenderer.material = new Material(Shader.Find("Sprites/Default")); // Simple line material
        lineRenderer.startColor = Color.black;
        lineRenderer.endColor = Color.black;

        DrawConnections();
    }

    public void SetColor(Color color)
    {
        regionColor = color;
        regionRenderer.material.color = color;
    }

    void DrawConnections()
    {
        if (neighbors.Count == 0) return;

        List<Vector3> linePoints = new List<Vector3>();

        foreach (Region neighbor in neighbors)
        {
            linePoints.Add(transform.position);
            linePoints.Add(neighbor.transform.position);
        }

        lineRenderer.positionCount = linePoints.Count;
        lineRenderer.SetPositions(linePoints.ToArray());
    }
}
