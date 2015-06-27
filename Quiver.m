(* ::Package:: *)

(* :Title: MyQuivers *)
(* :Authors: Day Zhou *)
(* :Version: 1.1.1 *)
(* :Context: MyQuivers` *)
(* :Copyleft: :D *)
(* Mathematica Version: 8.0.0 *)


BeginPackage["Quiver`"];
<< Combinatorica`;


(* Usage Information *)

CountQuiverNumber::usage = "CountQuiverNumber[n, e] gives the number of graphs for n vertices and e edges.";

DrawGraphs::usage = "DrawGraphs[n_Integer, e_Integer, num_List].\n \
DrawGraphs[n_Integer, e_Integer, k_Integer] = DrawGraphs[n, e, {k, k}]\n \
DrawGraphs[n_Integer, e_Integer] = DrawGraphs[n, e, {1, Infinity}].";

DrawNEScatter::usage = "DrawNEScatter[n_Integer, e_Integer] draws degree-dimension scatter plot for specific N and E of non-generic case.";
DrawGenericNEScatter::usage = "DrawGenericNEScatter[n_Integer, e_Integer] draws degree-dimension scatter plot for specific N and E for generic case.";

ListScatter::usage := "ListScatter[] list scatter table for non-generic case."
ListGenericScatter::usage := "ListGenericScatter[] list scatter table for generic case."

DrawScatter::usage = "DrawScatter[] draws total degree-dimension scatter plot for non-generic case.";
DrawGenericScatter::usage = "DrawScatter[name_String] draws total degree-dimension scatter plot for generic case.";

DrawDensityScatter::usage = "DrawScatter[n_Integer, e_Integer] draws the Degree-Dimension scatter plot."
DrawGenericDensityScatter::usage = "DrawGenericScatter[n_Integer, e_Integer] draws the generic Degree-Dimension scatter plot."

PresentStatisticTable::usage = "PresentStatisticTable[n_Integer, e_Integer, count_List] presents Dimension and Degree data of superpotentials for quivers of given n&e in a table form.";
PresentGenericStatisticTable::usage = "PresentGenericStatisticTable[n_Integer, e_Integer, count_List] presents Dimension and Degree data of generic superpotentials for quivers of given n&e in a table form.";

PresentData::usage = "PresentData[n, e, count_List, max] presents data in a readable form.\n \
\"n\" and \"e\" are the numbers of vertices and edges. \"count\" is an integral list determining which superpotentials to present. \"max\" determines the number above which histograms and charts are used instead of listing all the superpotentials.\n \
PresentData[n, e, count_Integer, max], \"count\" is an integer determining which one superpotential to present.\n \
PresentData[n, e, count_List] is equal to PresentData[n, e, count_List, 20].\n \
PresentData[n, e, count_Integer] is equal to PresentData[n, e, count_List, 20].\n \
PresentData[n, e, All, max] presents all the superpotentials and is equal to PresentData[n, e, {1, Infinity}, max]\n \
PresentData[n, e] is equal to PresentData[n, e, All, 20].";

PresentDimension::usage = "PresentDimension[n_Integer, e_Integer].";
PresentDegree::usage = "PresentDegree[n_Integer, e_Integer].";

PresentGenericData::usage = "PresentGenericData[n, e, count_List, max] presents data in a readable form. Refer to function: PresentData[].";
PresentGenericDimension::usage = "PresentGenericDimension[n_Integer, e_Integer].";
PresentGenericDegree::usage = "PresentGenericDegree[n_Integer, e_Integer].";

(*
ReadSuperPotentials::usage = "ReadSuperPotentials[n, e, count] reads in the superpotential list of n nodes and e edges. The argument \"e\" MUST be a list. If count<=0 or count is greater than the number of files, read all the superpotential list files.";
ReadTerms::usage = "ReadTerms[n, e, count] reads in the term list of n nodes and e edges. The argument \"e\" MUST be a list. If count<=0 or count is greater than the number of files, read all the term list files.";
ReadGIOs::usage = "ReadGIOs[n, e, count] reads in the GIO list of n nodes and e edges. The argument \"e\" MUST be a list. If count<=0 or count is greater than the number of files, read all the GIO list files.";
*)


Begin["`Private`"];

ToEdges[cycle_] := Table[{cycle[[i]], cycle[[i + 1]]}, {i, 1, Length[cycle] - 1}];

GraphFormat[n_, cycles_] := Module[{g},
	g = MakeGraph[Range[n], False &];
	g = AddEdges[g, Flatten[ToEdges[#] & /@ cycles, 1]];
	Return[g];
];

StyledGraph[ g_ ] := GraphPlot[ToAdjacencyMatrix[g], DirectedEdges -> True, VertexLabeling -> True, MultiedgeStyle -> True, SelfLoopStyle -> True, PlotStyle -> Black];

StyledPlot[g_] := Print[ StyledGraph[g] ];

neRootFolder[n_, e_] := FileNameJoin[{"DATA", "n=" <> ToString[n], "e=" <> ToString[e]}];

CountQuiverNumber[n_Integer, e_Integer] := Module[
	{neFolder = neRootFolder[n, e], fCount, quiverNumber},
	fCount = OpenRead[FileNameJoin[{neFolder, "count.txt"}]];
	quiverNumber = Read[fCount, Number];
	Close[fCount];
	Return[quiverNumber];
];

DrawGraphs[n_Integer, e_Integer, num_List] := Module[
	{neFolder = neRootFolder[n, e], min = Min[ num[[1]], num[[2]] ], max = Max[ num[[1]], num[[2]] ], count=CountQuiverNumber[n, e]},
	If[ min > count, Return[] ];
	max = Min[ max, count ];
	
	f = OpenRead[ FileNameJoin[{neFolder, "quiver.txt"}] ];
	For[ i = 1, i < min, i++, Read[f, String] ];
	For[ i = min, i <= max, i++,
		Print["----- ----- Graphs: ", i, " ----- -----"];
		g = GraphFormat[ n, ToExpression[ StringReplace[ Read[f, String], {"[" -> "{", "]" -> "}"}] ] + 1 ];
		StyledPlot[g];
	];
	Close[f];
];
DrawGraphs[n_Integer, e_Integer, k_Integer] := DrawGraphs[n, e, {k, k}];
DrawGraphs[n_Integer, e_Integer] := DrawGraphs[n, e, {1, Infinity}];

NumberToFileName[n_Integer, len_Integer] := Module[{},
	If[n >= 10^(len - 1), Return[ToString[n]]];
	Return[StringJoin[ToString /@ IntegerDigits[n, 10, len]]];
];

Mark[x_] := Which[
	x < 10, {0, 12},
	x >= 10 && x < 100, {1, 12},
	x >= 100 && x < 1000, {2, 12},
	x >= 1000 && x < 10000, {3, 12},
	x >= 10000 && x < 100000, {4, 12},
	x >= 100000 && x < 1000000, {5, 12},
	x >= 1000000 && x < 10000000, {6, 12},
	x >= 10000000 && x < 100000000, {7, 12},
	x >= 100000000 && x < 1000000000, {8, 12},
	x >= 1000000000 && x < 10000000000, {9, 12},
	x >= 10000000000, {10, 12}
];

DrawNEScatter[n_, e_, name_String] := Module[
	{ neFolder = neRootFolder[n, e], file, list, dimMin, dimMax, degMin, degMax, marks },
	file = FileNameJoin[{neFolder, name <> "deg-dim_math.txt"}];
	If[ ! FileExistsQ[file], Print["!!! Can not find scatter data file. !!!"]; Return[] ];
	
	list = ReadList[file, Expression][[1]];
	If[ list == {}, Print["!!! Empty data set. !!!"]; Return[] ];
	{degMin, degMax} = {Min[list[[All, 1]]], Max[list[[All, 1]]]};
	{dimMin, dimMax} = {Min[list[[All, 2]]], Max[list[[All, 2]]]};
	
	marks = Mark /@ Flatten[ list[[All, 3]] ];
	Print[ ListPlot[
		Table[{list[[i, 1 ;; 2]]}, {i, Length[list]}],
		PlotLabel -> ToString[n] <> "-" <> ToString[e] <> "-Degree-Dimension Scatter",
		AxesOrigin -> {0, -1},
		AxesLabel -> {"Deg", "Dim"},
		Ticks -> {Range[degMin, degMax], Range[dimMin, dimMax]},
		PlotRange -> All,
		PlotMarkers -> marks
	] ];
];
DrawNEScatter[n_Integer, e_Integer] := DrawNEScatter[n, e, ""];
DrawGenericNEScatter[n_Integer, e_Integer] := DrawNEScatter[n, e, "bg_"];

ListScatter[name_String] := Module[
	{file, list, degMin, degMax, dimMin, dimMax},
	file = FileNameJoin[{"DATA", name}];
	If[! FileExistsQ[file], Print["!!! Can not find scatter data file. !!!"]; Return[]];
	list = ReadList[file, Expression][[1]];
	If[list == {}, Print["!!! Empty data set. !!!"]; Return[]];
	list = Sort[list, #1[[3]] < #2[[3]] &];
	list = Append[list, {"", "", Plus @@ list[[All, 3]]}];
	list = Prepend[list, {"Degree", "Dimension", "Frequency"}];
	Print[Grid[list, Frame -> All]];
];
ListScatter[] := ListScatter["scatter.txt"];
ListGenericScatter[] := ListScatter["bg_scatter.txt"];

DrawScatter[name_String] := Module[
	{file, list, marks, degMin, degMax, dimMin, dimMax},
	file = FileNameJoin[{"DATA", name}];
	If[! FileExistsQ[file], 
	Print["!!! Can not find scatter data file. !!!"]; Return[]];
	list = ReadList[file, Expression][[1]];
	If[list == {}, Print["!!! Empty data set. !!!"]; Return[]];

	marks = Mark /@ Flatten[list[[All, 3]]];
	{degMin, degMax} = {Min[list[[All, 1]]], Max[list[[All, 1]]]};
	{dimMin, dimMax} = {Min[list[[All, 2]]], Max[list[[All, 2]]]};
	Print[ Show[ ListPlot[
		Table[{list[[i, 1 ;; 2]]}, {i, Length[list]}],
		PlotLabel -> "Degree-Dimension Scatter",
		AspectRatio -> 0.6,
		AxesOrigin -> {( 11 * degMin - degMax ) / 10, ( 7 * dimMin - dimMax ) / 6},
		AxesLabel -> {"Deg", "Dim"},
		Ticks -> {Range[degMin, degMax], Range[dimMin, dimMax]},
		PlotRange -> All,
		PlotMarkers -> marks
		] ,
		Plot[ 3.5, {x, 0.5, 3.5}, PlotStyle -> Dashed],
		ParametricPlot[ {3.5, y}, {y, -0.5, 3.5}, PlotStyle  -> Dashed]
	] ];
];
DrawScatter[] := DrawScatter["scatter.txt"];
DrawGenericScatter[] := DrawScatter["bg_scatter.txt"];

DrawDensityScatter[ name_String ] := Module[
	{file, list, degMin, degMax, dimMin, dimMax},
	file = FileNameJoin[{"DATA", name}];
	If[ ! FileExistsQ[file], Print["!!! Can not find scatter data file. !!!"]; Return[] ];
	
	list = ReadList[ file, Expression ][[1]];
	If[ list == {}, Print["!!! Empty data set. !!!"]; Return[] ];
	{degMin, degMax} = { Min[ list[[All, 1]] ], Max[ list[[All, 1]] ] };
	{dimMin, dimMax} = {Min[ list[[All, 2]] ], Max[ list[[All, 2]] ] };
	
	Print[
		ListDensityPlot[ list,
			PlotLabel -> "Degree-Dimension Density Scatter",
			AspectRatio -> 0.6,
			Axes -> True,
			AxesOrigin -> {( 11 * degMin - degMax ) / 10, ( 7 * dimMin - dimMax ) / 6},
			AxesLabel -> {"Deg", "Dim"},
			Frame -> False,
			Ticks -> {Range[degMin, degMax], Range[dimMin, dimMax]},
			PlotRange -> All,
			MeshStyle -> {Dashed, Dashed},
			Mesh -> {degMax - degMin - 1, dimMax - dimMin - 1}
		]
	];
];
DrawDensityScatter[] := DrawDensityScatter[ "scatter.txt" ];
DrawGenericDensityScatter[] := DrawDensityScatter[ "bg_scatter.txt" ];

PresentStatisticTable[n_Integer, e_Integer, count_List] := Module[
	{ neFolder = neRootFolder[n, e], prFolder, prNumber, prName, quiverNumber, i, fpr, list,
	statistics = {{"Quiver", "Dim | Count", "Deg | Count"}}, graph, dimMin, dimMax, degMin, degMax, dimCount, degCount, dimTable, degTable},
	prFolder = FileNameJoin[{neFolder, "present"}];
	quiverNumber = CountQuiverNumber[n, e];
	If[ count[[1]] > quiverNumber, Return[] ];

	For[ i = count[[1]], i <= Min[count[[2]], quiverNumber], i++,
		prNumber = NumberToFileName[i, 6];
		prName = FileNameJoin[{prFolder, prNumber <> ".txt"}];
		If[ ! FileExistsQ[prName],
			prName = FileNameJoin[{prFolder, prNumber <> "_r.txt"}];
			If[ ! FileExistsQ[prName], Print["No super-potential data are found."]; Continue[] ];
		];
		
		fpr = OpenRead[prName];
		graph = StyledGraph[GraphFormat[n, Read[fpr, Expression]]];
		list = ReadList[fpr, Expression];
		Close[fpr];
		
		{dimMin, dimMax} = {Min[list[[All, 2]]], Max[list[[All, 2]]]};
		{degMin, degMax} = {Min[list[[All, 3]]], Max[list[[All, 3]]]};
		dimCount = BinCounts[list[[All, 2]], {dimMin, dimMax + 1}];
		degCount = BinCounts[list[[All, 3]], {degMin, degMax + 1}];
		dimTable = TableForm[ Table[ {k, dimCount[[k+1-dimMin]]}, {k, dimMin, dimMax} ], TableHeadings -> {None, {"Dim", "Count"}}, TableAlignments -> {Center, None}];
		degTable = TableForm[ Table[ {k, degCount[[k+1-degMin]]}, {k, degMin, degMax} ], TableHeadings -> {None, {"Deg", "Count"}}, TableAlignments -> {Center, None}];
		
		statistics = Append[ statistics, {graph, dimTable, degTable} ];
	];
	Print[ Grid[ statistics, Frame -> All ] ];
];
PresentStatisticTable[n_Integer, e_Integer, count_Integer] := PresentStatisticTable[n, e, {count, count}];
PresentStatisticTable[n_Integer, e_Integer] := PresentStatisticTable[n, e, {1, Infinity}];

PresentGenericStatisticTable[n_Integer, e_Integer, count_List] := Module[
	{ neFolder = neRootFolder[n, e], prFolder, prNumber, prName, quiverNumber, i, fpr, list,
	statistics = {{"Quiver", "Dim | Count", "Deg | Count"}}, graph, dimMin, dimMax, degMin, degMax, dimCount, degCount, dimTable, degTable},
	prFolder = FileNameJoin[{neFolder, "bg_present"}];
	quiverNumber = CountQuiverNumber[n, e];
	If[ count[[1]] > quiverNumber, Return[] ];

	For[ i = count[[1]], i <= Min[count[[2]], quiverNumber], i++,
		prNumber = NumberToFileName[i, 6];
		prName = FileNameJoin[{prFolder, prNumber <> "_bg.txt"}];
		If[ ! FileExistsQ[prName],
			prName = FileNameJoin[{prFolder, prNumber <> "_bg_r.txt"}];
			If[ ! FileExistsQ[prName], Continue[] ];
		];
		
		fpr = OpenRead[prName];
		graph = StyledGraph[GraphFormat[n, Read[fpr, Expression]]];
		list = ReadList[fpr, Expression];
		Close[fpr];
		
		{dimMin, dimMax} = { Min[ list[[All, 2]] ], Max[ list[[All, 2]] ] };
		{degMin, degMax} = { Min[ list[[All, 3]] ], Max[ list[[All, 3]] ] };
		dimCount = BinCounts[ list[[All, 2]], {dimMin, dimMax + 1} ];
		degCount = BinCounts[ list[[All, 3]], {degMin, degMax + 1} ];
		dimTable = TableForm[ Table[ {k, dimCount[[k+1-dimMin]]}, {k, dimMin, dimMax} ], TableHeadings -> {None, {"Dim", "Count"}}, TableAlignments -> {Center, None}];
		degTable = TableForm[ Table[ {k, degCount[[k+1-degMin]]}, {k, degMin, degMax} ], TableHeadings -> {None, {"Deg", "Count"}}, TableAlignments -> {Center, None}];
		
		statistics = Append[ statistics, {graph, dimTable, degTable} ];
	];
	Print[ Grid[ statistics, Frame -> All ] ];
];
PresentGenericStatisticTable[n_Integer, e_Integer, count_Integer] := PresentGenericStatisticTable[n, e, {count, count}];
PresentGenericStatisticTable[n_Integer, e_Integer] := PresentGenericStatisticTable[n, e, {1, Infinity}];

DrawStatistics[list_] := Module[
	{TotalTheories = Length[list], count, dimMin, dimMax, degMin, degMax},

	{dimMin, dimMax} = {Min[list[[All, 2]]], Max[list[[All, 2]]]};
	count = BinCounts[list[[All, 2]], {dimMin, dimMax + 1}];
	Print[BarChart[count, BarSpacing -> None, ChartLabels -> Range[dimMin, dimMax], PlotLabel -> "Dimension Histogram", AxesLabel -> {"Dim", "Freq"}, LabelingFunction -> Above]];
	Print[BarChart[N[count/TotalTheories, 4], BarSpacing -> None, ChartLabels -> Range[dimMin, dimMax], PlotLabel -> "Proportion of Quiver Theories of Each Dimension", AxesLabel -> {"Dim", "Perc"}, LabelingFunction -> Above]];

	{degMin, degMax} = {Min[list[[All, 3]]], Max[list[[All, 3]]]};
	count = BinCounts[list[[All, 3]], {degMin, degMax + 1}];
	Print[BarChart[count, BarSpacing -> None, ChartLabels -> Range[degMin, degMax], PlotLabel -> "Degree Histogram", AxesLabel -> {"Deg", "Freq"}, LabelingFunction -> Above]];
	Print[BarChart[N[count/TotalTheories, 4], BarSpacing -> None, ChartLabels -> Range[degMin, degMax], PlotLabel -> "Proportion of Quiver Theories of Each Degree", AxesLabel -> {"Deg", "Perc"}, LabelingFunction -> Above]];

	Print[ ListPlot[
		Reverse[ list[[All, 2 ;; 3]], 2],
		PlotLabel -> "Degree vs. Dimension Scatter",
		AxesLabel -> {"Deg", "Dim"},
		AxesOrigin -> {0, 0},
		PlotStyle -> PointSize[.02],
		Ticks -> {Range[degMin, degMax], Range[dimMin, dimMax]},
		PlotRange -> All
	] ];
];

PresentData[n_Integer, e_Integer, count_List, max_Integer] := Module[
	{neFolder = neRootFolder[n, e], prFolder, quiverNumber, i, fpr, list, prNumber, prName},
	prFolder = FileNameJoin[{neFolder, "present"}];
	quiverNumber = CountQuiverNumber[n, e];
	If[ count[[1]] > quiverNumber, Return[] ];

	For[i = count[[1]], i <= Min[count[[2]], quiverNumber], i++,
		Print[ StringForm["\n---------- ---------- QUIVER: `` --- n: `` --- e: `` ---------- ----------", i, n, e] ];
		prNumber = NumberToFileName[i, 6];
		prName = FileNameJoin[{prFolder, prNumber <> ".txt"}];
		If[ ! FileExistsQ[prName],
			prName = FileNameJoin[{prFolder, prNumber <> "_r.txt"}];
			If[ ! FileExistsQ[prName], Print["No super-potential data are found."]; Continue[] ];
		];
		
		fpr = OpenRead[prName];
		StyledPlot[GraphFormat[n, Read[fpr, Expression]]];
		list = ReadList[fpr, Expression];
		Close[fpr];

		If[ Length[list] < max,
			Print[ TableForm[ list, TableHeadings -> {Range[ Length[list] ], {"Superpotential", "Dimension", "Degree"}}] ];
			,
			DrawStatistics[list];
		];
	];
];

PresentData[n_Integer, e_Integer, count_Integer, max_Integer] := PresentData[n, e, {count, count}, max];
PresentData[n_Integer, e_Integer, count_List] := PresentData[n, e, count, 20];
PresentData[n_Integer, e_Integer, count_Integer] := PresentData[n, e, {count, count}, 20];
PresentData[n_Integer, e_Integer, All, max_Integer] := PresentData[n, e, {1, Infinity}, max];
PresentData[n_Integer, e_Integer] := PresentData[n, e, {1, Infinity}, 20];

PresentDimension[n_Integer, e_Integer] := Module[
	{neFolder = neRootFolder[n, e], dimList},
	dimList = ReadList[ FileNameJoin[{neFolder, "dimension.txt"}], Expression][[1]];
	Print[ TableForm[ dimList, TableHeadings -> {None, {"Dim", "Perc(%)"}}, TableAlignments -> {Center, None}] ];
];

PresentDegree[n_Integer, e_Integer] := Module[
	{neFolder = neRootFolder[n, e], degList},
	degList = ReadList[ FileNameJoin[{neFolder, "degree.txt"}], Expression][[1]];
	Print[ TableForm[ degList, TableHeadings -> {None, {"Deg", "Perc(%)"}}, TableAlignments -> {Center, None}] ];
];


PresentGenericData[n_Integer, e_Integer, count_List, max_Integer] := Module[
	{neFolder = neRootFolder[n, e], prFolder, quiverNumber, i, fpr, list, prNumber, prName},
	prFolder = FileNameJoin[{neFolder, "bg_present"}];
	quiverNumber = CountQuiverNumber[n, e];
	If[ count[[1]] > quiverNumber, Return[] ];

	For[i = count[[1]], i <= Min[count[[2]], quiverNumber], i++,
		Print[ StringForm["\n---------- ---------- QUIVER: `` --- n: `` --- e: `` ---------- ----------", i, n, e] ];
		prNumber = NumberToFileName[i, 6];
		prName = FileNameJoin[{prFolder, prNumber <> "_bg.txt"}];
		If[ ! FileExistsQ[prName],
			prName = FileNameJoin[{prFolder, prNumber <> "_bg_r.txt"}];
			If[ ! FileExistsQ[prName], Print["No generic super-potential data are found."]; Continue[] ];
		];
		
		fpr = OpenRead[prName];
		StyledPlot[GraphFormat[n, Read[fpr, Expression]]];
		list = ReadList[fpr, Expression];
		Close[fpr];

		If[ Length[list] < max,
			Print[ TableForm[ list, TableHeadings -> {Range[ Length[list] ], {"Generic-Superpotential", "Generic-Dimension", "Generic-Degree"}}] ];
			,
			DrawStatistics[list];
		];
	];
];

PresentGenericData[n_Integer, e_Integer, count_Integer, max_Integer] := PresentGenericData[n, e, {count, count}, max];
PresentGenericData[n_Integer, e_Integer, count_List] := PresentGenericData[n, e, count, 20];
PresentGenericData[n_Integer, e_Integer, count_Integer] := PresentGenericData[n, e, {count, count}, 20];
PresentGenericData[n_Integer, e_Integer, All, max_Integer] := PresentGenericData[n, e, {1, Infinity}, max];
PresentGenericData[n_Integer, e_Integer] := PresentGenericData[n, e, {1, Infinity}, 20];

PresentGenericDimension[n_Integer, e_Integer] := Module[
	{neFolder = neRootFolder[n, e], dimList},
	dimList = ReadList[ FileNameJoin[{neFolder, "bg_dimension.txt"}], Expression][[1]];
	Print[ TableForm[ dimList, TableHeadings -> {None, {"Generic-Dim", "Perc(%)"}}, TableAlignments -> {Center, None}] ];
];

PresentGenericDegree[n_Integer, e_Integer] := Module[
	{neFolder = neRootFolder[n, e], degList},
	degList = ReadList[ FileNameJoin[{neFolder, "bg_degree.txt"}], Expression][[1]];
	Print[ TableForm[ degList, TableHeadings -> {None, {"Generic-Deg", "Perc(%)"}}, TableAlignments -> {Center, None}] ];
];

(* --------------------------------------------------------------------------------------------- unused and not functional

ReadGIOs[n_Integer, e_, count_] := Module[
	{list, len, num = count, i},
	If[ ArgumentsAreNotValid[n, e], Print[ReadInNothing]; Return[] ];

	FileNameDictionary = GenerateFileNameDict[n, e];
	list = Select[ FileNames["*", FileDict["DataFolder"]], StringMatchQ[#, FileDict["GIOFile"] ~~ __] &];
	len = Length[list];

	If[ count <= 0 || count > len, num = len];
	For[i = 1, i <= num, i++,
		Print[ "File Name: \"", list[[i]], "\"" ];
		Print[ TableForm[ ReadList[ list[[i]], Expression] ] ];
	];
];

ReadSuperPotentials[n_Integer, e_, count_Integer] := Module[
	{list, len, num = count, i},
	If[ ArgumentsAreNotValid[n, e], Print[ReadInNothing]; Return[] ];

	FileNameDictionary = GenerateFileNameDict[n, e];
	list = Select[ FileNames["*", FileDict["DataFolder"]], StringMatchQ[#, FileDict["PotentialFile"] ~~ __] &];
	len = Length[list];

	If[ count <= 0 || count > len, num = len];
	For[ i = 1, i <= num, i++,
		Print[ "File Name: \"", list[[i]], "\"" ];
		Print[ TableForm[ ReadList[ list[[i]], Expression] ] ];
	];
];

ReadTerms[n_Integer, e_, count_] := Module[
	{list, len, num = count, i},
	If[ ArgumentsAreNotValid[n, e], Print[ReadInNothing]; Return[] ];

	FileNameDictionary = GenerateFileNameDict[n, e];
	list = Select[ FileNames["*", FileDict["DataFolder"]], StringMatchQ[#, FileDict["TermFile"] ~~ __] &];
	len = Length[list];

	If[ count <= 0 || count > len, num = len];
	For[i = 1, i <= num, i++,
		Print[ "File Name: \"", list[[i]], "\"" ];
		Print[ TableForm[ ReadList[ list[[i]], Expression] ] ];
	];
];

*)

End[];


EndPackage[];
