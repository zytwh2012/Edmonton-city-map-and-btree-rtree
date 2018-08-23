CREATE VIRTUAL TABLE areaMBRTree USING rtree(
    id,
    minX,maxX,
    minY,maxY
);
INSERT INTO areaMBRTree SELECT * FROM areaMBR;
.exit
