import OrderedCollections
import PathKit
import XcodeProj

extension Generator {
    /// Creates an array of `XCScheme` entries for the specified targets.
    static func createAutogeneratedXCSchemes(
        schemeAutogenerationMode: SchemeAutogenerationMode,
        buildMode: BuildMode,
        targetResolver: TargetResolver,
        customSchemeNames: Set<String>
    ) throws -> [XCScheme] {
        let shouldAutogenerateSchemes: Bool
        switch schemeAutogenerationMode {
        case .none:
            shouldAutogenerateSchemes = false
        case .all:
            shouldAutogenerateSchemes = true
        case .auto:
            shouldAutogenerateSchemes = customSchemeNames.isEmpty
        }
        guard shouldAutogenerateSchemes else {
            return []
        }

        return try targetResolver
            .targetInfos.filter(\.pbxTarget.shouldCreateScheme)
            .map { targetInfo in
                let pbxTarget = targetInfo.pbxTarget
                let buildConfigurationName = pbxTarget.defaultBuildConfigurationName

                let shouldCreateTestAction = pbxTarget.isTestable
                let shouldCreateLaunchAction = pbxTarget.isLaunchable
                let schemeInfo = try XCSchemeInfo(
                    buildActionInfo: .init(targetInfos: [targetInfo]),
                    testActionInfo: shouldCreateTestAction ?
                        .init(
                            buildConfigurationName: buildConfigurationName,
                            targetInfos: [targetInfo]
                        ) : nil,
                    launchActionInfo: shouldCreateLaunchAction ?
                        .init(
                            buildConfigurationName: buildConfigurationName,
                            targetInfo: targetInfo
                        ) : nil,
                    profileActionInfo: shouldCreateLaunchAction ?
                        .init(
                            buildConfigurationName: buildConfigurationName,
                            targetInfo: targetInfo
                        ) : nil,
                    analyzeActionInfo: .init(buildConfigurationName: buildConfigurationName),
                    archiveActionInfo: .init(buildConfigurationName: buildConfigurationName)
                ) { buildActionInfo, _, _, _ in
                    guard let targetInfo = buildActionInfo?.targetInfos.first else {
                        throw PreconditionError(message: """
    Expected to find a `TargetInfo` in the `BuildActionInfo`.
    """)
                    }
                    let schemeName: String
                    if let selectedHostInfo = try targetInfo.selectedHostInfo,
                        targetInfo.disambiguateHost
                    {
                        schemeName = """
    \(targetInfo.pbxTarget.schemeName) in \(selectedHostInfo.pbxTarget.schemeName)
    """
                    } else {
                        schemeName = targetInfo.pbxTarget.schemeName
                    }
                    return schemeName
                }

                return try XCScheme(buildMode: buildMode, schemeInfo: schemeInfo)
            }
    }
}
