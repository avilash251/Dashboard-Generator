// src/utils/infraAdapter.js
export function adaptInfra(layout) {
  // Expecting layout.assets like [{type:"tkgi", name:"Cluster A", nodes:12, cpu:"64C"}]
  const buckets = { tkgi:[], ocp:[], tas:[], onprem:[], database:[], network:[], gcp:[], azure:[] };

  (layout?.assets || []).forEach((a, i) => {
    const k = (a.type || "").replace("-", "") || "onprem";
    buckets[k] = buckets[k] || [];
    buckets[k].push({
      id: `${k}:${a.id ?? i}`,
      name: a.name ?? `${k} item ${i+1}`,
      subtitle:
        a.subtitle ??
        [
          a.nodes ? `${a.nodes} nodes` : null,
          a.cpu ? `${a.cpu} CPU` : null,
          a.memory ? `${a.memory} GB RAM` : null,
        ]
          .filter(Boolean)
          .join(", "),
      raw: a,
    });
  });

  return buckets;
}
